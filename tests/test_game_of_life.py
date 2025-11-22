"""
Tests for Conway's Game of Life - Grid Module
"""

import pytest
from game_of_life.grid import Grid
from game_of_life.game_engine import GameOfLife


class TestGridInitialization:
    """Test grid creation and initialization."""

    def test_grid_creation(self):
        """Grid should be created with specified dimensions."""
        grid = Grid(10, 20)
        assert grid.width == 10
        assert grid.height == 20

    def test_grid_starts_empty(self):
        """All cells should start as dead (False)."""
        grid = Grid(5, 5)
        for y in range(5):
            for x in range(5):
                assert grid.get_cell(x, y) == False

    def test_invalid_dimensions(self):
        """Should raise ValueError for invalid dimensions."""
        with pytest.raises(ValueError):
            Grid(0, 10)
        with pytest.raises(ValueError):
            Grid(10, 0)
        with pytest.raises(ValueError):
            Grid(-5, 10)


class TestCellOperations:
    """Test setting and getting individual cells."""

    def test_set_cell_alive(self):
        """Should be able to set a cell to alive."""
        grid = Grid(5, 5)
        grid.set_cell(2, 3, True)
        assert grid.get_cell(2, 3) == True

    def test_set_cell_dead(self):
        """Should be able to set a cell to dead."""
        grid = Grid(5, 5)
        grid.set_cell(1, 1, True)
        grid.set_cell(1, 1, False)
        assert grid.get_cell(1, 1) == False

    def test_out_of_bounds_get(self):
        """Should raise IndexError for out of bounds coordinates."""
        grid = Grid(5, 5)
        with pytest.raises(IndexError):
            grid.get_cell(5, 5)  # Valid range is 0-4
        with pytest.raises(IndexError):
            grid.get_cell(-1, 0)


class TestNeighborCounting:
    """Test neighbor counting logic (critical for Conway's rules)."""

    def test_no_neighbors(self):
        """Cell with no living neighbors should count 0."""
        grid = Grid(5, 5)
        assert grid.count_neighbors(2, 2) == 0

    def test_one_neighbor(self):
        """Cell with one living neighbor should count 1."""
        grid = Grid(5, 5)
        grid.set_cell(1, 1, True)  # Set neighbor alive
        assert grid.count_neighbors(2, 2) == 1

    def test_all_neighbors_alive(self):
        """Cell surrounded by all alive cells should count 8."""
        grid = Grid(5, 5)
        # Set all 8 neighbors alive around cell (2,2)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the center cell
                grid.set_cell(2 + dx, 2 + dy, True)

        assert grid.count_neighbors(2, 2) == 8

    def test_corner_wrapping(self):
        """Corner cells should wrap around edges (toroidal grid)."""
        grid = Grid(5, 5)
        # Place a cell at bottom-right corner
        grid.set_cell(4, 4, True)

        # Top-left corner should see it as a neighbor due to wrapping
        assert grid.count_neighbors(0, 0) == 1


class TestGameOfLifeEngine:
    """Test Conway's Game of Life rules engine."""

    def test_game_initialization(self):
        """Game should initialize with empty grid at generation 0."""
        game = GameOfLife(10, 10)
        assert game.get_generation() == 0
        assert game.get_living_cells() == 0
        assert game.width == 10
        assert game.height == 10

    def test_conway_rule_survival(self):
        """Living cell with 2-3 neighbors should survive."""
        game = GameOfLife(5, 5)

        # Test with 2 neighbors (should survive)
        assert game._apply_conway_rules(is_alive=True, neighbor_count=2) == True

        # Test with 3 neighbors (should survive)
        assert game._apply_conway_rules(is_alive=True, neighbor_count=3) == True

    def test_conway_rule_death_loneliness(self):
        """Living cell with <2 neighbors should die."""
        game = GameOfLife(5, 5)

        # Test with 0 neighbors (should die)
        assert game._apply_conway_rules(is_alive=True, neighbor_count=0) == False

        # Test with 1 neighbor (should die)
        assert game._apply_conway_rules(is_alive=True, neighbor_count=1) == False

    def test_conway_rule_death_overcrowding(self):
        """Living cell with >3 neighbors should die."""
        game = GameOfLife(5, 5)

        # Test with 4 neighbors (should die)
        assert game._apply_conway_rules(is_alive=True, neighbor_count=4) == False

        # Test with 5 neighbors (should die)
        assert game._apply_conway_rules(is_alive=True, neighbor_count=5) == False

        # Test with 8 neighbors (should die)
        assert game._apply_conway_rules(is_alive=True, neighbor_count=8) == False

    def test_conway_rule_birth(self):
        """Dead cell with exactly 3 neighbors should become alive."""
        game = GameOfLife(5, 5)

        # Test with 3 neighbors (should be born)
        assert game._apply_conway_rules(is_alive=False, neighbor_count=3) == True

        # Test with other neighbor counts (should stay dead)
        assert game._apply_conway_rules(is_alive=False, neighbor_count=0) == False
        assert game._apply_conway_rules(is_alive=False, neighbor_count=1) == False
        assert game._apply_conway_rules(is_alive=False, neighbor_count=2) == False
        assert game._apply_conway_rules(is_alive=False, neighbor_count=4) == False


class TestNextGenerationIntegration:
    """Test next_generation() method with various scenarios."""

    def test_empty_grid_stays_empty(self):
        """Empty grid should remain empty after next_generation."""
        game = GameOfLife(5, 5)
        # Grid starts empty
        assert game.get_living_cells() == 0
        assert game.get_generation() == 0

        game.next_generation()

        # Should still be empty (no births possible)
        assert game.get_living_cells() == 0
        assert game.get_generation() == 1

    def test_single_cell_dies(self):
        """Single isolated cell should die from loneliness."""
        game = GameOfLife(5, 5)
        game.grid.set_cell(2, 2, True)  # Place one cell in center

        assert game.get_living_cells() == 1
        assert game.get_generation() == 0

        game.next_generation()

        # Cell should die (0 neighbors < 2 = loneliness)
        assert game.get_living_cells() == 0
        assert game.get_generation() == 1
        assert game.grid.get_cell(2, 2) == False

    def test_two_cells_both_die(self):
        """Two adjacent cells should both die from loneliness."""
        game = GameOfLife(5, 5)
        game.grid.set_cell(2, 2, True)  # First cell
        game.grid.set_cell(2, 3, True)  # Adjacent cell

        assert game.get_living_cells() == 2

        game.next_generation()

        # Both should die (each has only 1 neighbor < 2)
        assert game.get_living_cells() == 0
        assert game.get_generation() == 1

    def test_blinker_pattern_oscillation(self):
        """Test the famous Blinker pattern oscillates correctly."""
        game = GameOfLife(5, 5)

        # Set up horizontal blinker in center: ● ● ●
        game.grid.set_cell(1, 2, True)  # Left
        game.grid.set_cell(2, 2, True)  # Center
        game.grid.set_cell(3, 2, True)  # Right

        assert game.get_living_cells() == 3

        # After 1 generation: should become vertical blinker
        game.next_generation()

        assert game.get_living_cells() == 3  # Still 3 cells
        assert game.get_generation() == 1

        # Check it's now vertical: center column
        assert game.grid.get_cell(2, 1) == True  # Above center
        assert game.grid.get_cell(2, 2) == True  # Center (survives)
        assert game.grid.get_cell(2, 3) == True  # Below center

        # Horizontal positions should be dead
        assert game.grid.get_cell(1, 2) == False  # Left
        assert game.grid.get_cell(3, 2) == False  # Right

        # After another generation: should return to horizontal
        game.next_generation()

        assert game.get_living_cells() == 3  # Still 3 cells
        assert game.get_generation() == 2

        # Should be back to horizontal
        assert game.grid.get_cell(1, 2) == True  # Left
        assert game.grid.get_cell(2, 2) == True  # Center
        assert game.grid.get_cell(3, 2) == True  # Right

        # Vertical positions should be dead
        assert game.grid.get_cell(2, 1) == False  # Above
        assert game.grid.get_cell(2, 3) == False  # Below


class TestVisualizer:
    """Test the ASCII visualization system for Conway's Game of Life."""

    def test_visualizer_imports(self):
        """Visualizer class should be importable."""
        from game_of_life.visualizer import Visualizer

        visualizer = Visualizer()
        assert visualizer is not None

    def test_display_empty_grid(self):
        """Should display empty 3x3 grid with dead cell symbols."""
        from game_of_life.visualizer import Visualizer

        grid = Grid(3, 3)
        visualizer = Visualizer()

        output = visualizer.display_grid(grid, generation=0)

        # Should contain dead cell symbols
        assert "○" in output
        # Should not contain alive cell symbols
        assert "●" not in output
        # Should show generation counter
        assert "Generation: 0" in output

    def test_display_grid_with_alive_cells(self):
        """Should display grid with both alive and dead cells."""
        from game_of_life.visualizer import Visualizer

        grid = Grid(3, 3)
        grid.set_cell(1, 1, True)  # Center cell alive
        visualizer = Visualizer()

        output = visualizer.display_grid(grid, generation=5)

        # Should contain both symbols
        assert "●" in output  # Alive cells
        assert "○" in output  # Dead cells
        # Should show generation
        assert "Generation: 5" in output

    def test_display_statistics(self):
        """Should display population statistics."""
        from game_of_life.visualizer import Visualizer

        grid = Grid(3, 3)
        grid.set_cell(0, 0, True)
        grid.set_cell(2, 2, True)
        visualizer = Visualizer()

        output = visualizer.display_grid(grid, generation=1)

        # Should show population count
        assert "Population: 2" in output
        # Should show total cells
        assert "9" in output  # 3x3 = 9 total cells

    def test_blinker_pattern_visualization(self):
        """Should properly display the famous Blinker pattern."""
        from game_of_life.visualizer import Visualizer

        grid = Grid(5, 5)

        # Set up Blinker pattern (horizontal)
        grid.set_cell(1, 2, True)
        grid.set_cell(2, 2, True)
        grid.set_cell(3, 2, True)

        visualizer = Visualizer()
        output = visualizer.display_grid(grid, generation=0)

        # Should show horizontal line of alive cells
        lines = output.split("\n")
        grid_lines = [line for line in lines if "●" in line or "○" in line]
        assert len(grid_lines) == 5  # 5x5 grid

        # Middle row should have three alive cells
        middle_row = grid_lines[2]
        assert middle_row.count("●") == 3


class TestVisualizerGameIntegration:
    """Test visualizer integration with GameOfLife engine for animated simulation."""

    def test_visualizer_with_game_evolution(self):
        """Should track visualization changes as game evolves."""
        from game_of_life.visualizer import Visualizer
        from game_of_life.game_engine import GameOfLife

        # Create game with Blinker pattern
        game = GameOfLife(5, 5)
        game.grid.set_cell(1, 2, True)
        game.grid.set_cell(2, 2, True)
        game.grid.set_cell(3, 2, True)

        visualizer = Visualizer()

        # Generation 0 - horizontal
        gen0_display = visualizer.display_grid(game.grid, generation=0)
        assert "Generation: 0" in gen0_display
        assert "Population: 3" in gen0_display

        # Evolution to Generation 1 - vertical
        game.next_generation()
        gen1_display = visualizer.display_grid(game.grid, generation=1)
        assert "Generation: 1" in gen1_display
        assert "Population: 3" in gen1_display

        # Displays should be different (pattern changed)
        assert gen0_display != gen1_display

    def test_multi_generation_animation_sequence(self):
        """Should handle multiple generation evolution for animation."""
        from game_of_life.visualizer import Visualizer
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(5, 5)
        visualizer = Visualizer()

        # Set up Blinker pattern
        game.grid.set_cell(1, 2, True)
        game.grid.set_cell(2, 2, True)
        game.grid.set_cell(3, 2, True)

        # Collect displays for multiple generations
        displays = []
        for generation in range(4):  # 0, 1, 2, 3
            display = visualizer.display_grid(game.grid, generation=generation)
            displays.append(display)

            # Verify each display has correct generation number
            assert f"Generation: {generation}" in display

            if generation < 3:  # Don't evolve after last generation
                game.next_generation()

        # Should have 4 different displays
        assert len(displays) == 4

        # Blinker oscillates with period 2, so gen 0 == gen 2
        gen0_grid_lines = [
            line for line in displays[0].split("\n") if "●" in line or "○" in line
        ]
        gen2_grid_lines = [
            line for line in displays[2].split("\n") if "●" in line or "○" in line
        ]
        assert gen0_grid_lines == gen2_grid_lines  # Same pattern

        # Gen 1 and gen 3 should also be the same (vertical orientation)
        gen1_grid_lines = [
            line for line in displays[1].split("\n") if "●" in line or "○" in line
        ]
        gen3_grid_lines = [
            line for line in displays[3].split("\n") if "●" in line or "○" in line
        ]
        assert gen1_grid_lines == gen3_grid_lines  # Same pattern

    def test_population_tracking_through_generations(self):
        """Should track population changes through generations."""
        from game_of_life.visualizer import Visualizer
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(7, 7)
        visualizer = Visualizer()

        # Start with single cell (will die)
        game.grid.set_cell(3, 3, True)

        # Generation 0: 1 alive cell
        gen0_display = visualizer.display_grid(game.grid, generation=0)
        assert "Population: 1 / 49" in gen0_display  # 7x7 = 49

        # Generation 1: 0 alive cells (single cell dies)
        game.next_generation()
        gen1_display = visualizer.display_grid(game.grid, generation=1)
        assert "Population: 0 / 49" in gen1_display

        # Verify population correctly tracked
        assert "Population: 1" in gen0_display
        assert "Population: 0" in gen1_display

    def test_clear_screen_functionality(self):
        """Should provide screen clearing for animation."""
        from game_of_life.visualizer import Visualizer
        from game_of_life.grid import Grid

        visualizer = Visualizer()
        grid = Grid(3, 3)

        # Should not raise any exceptions
        try:
            visualizer.clear_screen()
            visualizer.print_grid(grid, generation=0, clear=True)
            visualizer.print_grid(grid, generation=0, clear=False)
        except Exception as e:
            pytest.fail(f"Screen clearing functionality failed: {e}")


class TestPatternLibrary:
    """Test the famous pattern library for Conway's Game of Life."""

    def test_pattern_library_imports(self):
        """Pattern library should be importable."""
        from game_of_life.patterns import PatternLibrary

        assert PatternLibrary is not None

    def test_blinker_pattern_creation(self):
        """Should create Blinker oscillator pattern correctly."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(7, 7)
        PatternLibrary.create_blinker(game, 3, 3)

        # Should have 3 alive cells in horizontal line
        assert game.grid.get_cell(2, 3) == True  # Left
        assert game.grid.get_cell(3, 3) == True  # Center
        assert game.grid.get_cell(4, 3) == True  # Right

        # Count total alive cells
        alive_count = sum(
            1 for y in range(7) for x in range(7) if game.grid.get_cell(x, y)
        )
        assert alive_count == 3

    def test_block_pattern_creation(self):
        """Should create Block still life pattern correctly."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(5, 5)
        PatternLibrary.create_block(game, 1, 1)

        # Should have 2x2 block
        assert game.grid.get_cell(1, 1) == True  # Top-left
        assert game.grid.get_cell(2, 1) == True  # Top-right
        assert game.grid.get_cell(1, 2) == True  # Bottom-left
        assert game.grid.get_cell(2, 2) == True  # Bottom-right

        # Count total alive cells
        alive_count = sum(
            1 for y in range(5) for x in range(5) if game.grid.get_cell(x, y)
        )
        assert alive_count == 4

    def test_glider_pattern_creation(self):
        """Should create Glider spaceship pattern correctly."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(7, 7)
        PatternLibrary.create_glider(game, 1, 1)

        # Glider should have 5 specific cells alive
        expected_cells = [(2, 1), (3, 2), (1, 3), (2, 3), (3, 3)]

        for x, y in expected_cells:
            assert game.grid.get_cell(x, y) == True, f"Cell ({x},{y}) should be alive"

        # Count total alive cells
        alive_count = sum(
            1 for y in range(7) for x in range(7) if game.grid.get_cell(x, y)
        )
        assert alive_count == 5

    def test_beehive_pattern_creation(self):
        """Should create Beehive still life pattern correctly."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(7, 7)
        PatternLibrary.create_beehive(game, 3, 3)

        # Beehive should have 6 cells in hexagonal shape
        expected_cells = [(3, 2), (4, 2), (2, 3), (5, 3), (3, 4), (4, 4)]

        for x, y in expected_cells:
            assert game.grid.get_cell(x, y) == True, f"Cell ({x},{y}) should be alive"

        # Count total alive cells
        alive_count = sum(
            1 for y in range(7) for x in range(7) if game.grid.get_cell(x, y)
        )
        assert alive_count == 6

    def test_pattern_info_retrieval(self):
        """Should provide information about available patterns."""
        from game_of_life.patterns import PatternLibrary

        info = PatternLibrary.get_pattern_info()

        # Should have all expected patterns
        expected_patterns = [
            "blinker",
            "block",
            "beehive",
            "toad",
            "beacon",
            "glider",
            "loaf",
        ]
        for pattern in expected_patterns:
            assert pattern in info
            assert "name" in info[pattern]
            assert "type" in info[pattern]
            assert "period" in info[pattern]
            assert "emoji" in info[pattern]

    def test_create_pattern_by_name(self):
        """Should create patterns by name using generic method."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(7, 7)

        # Test creating Blinker by name
        success = PatternLibrary.create_pattern("blinker", game, 3, 3)
        assert success == True

        # Verify pattern was created
        alive_count = sum(
            1 for y in range(7) for x in range(7) if game.grid.get_cell(x, y)
        )
        assert alive_count == 3

    def test_create_pattern_with_default_position(self):
        """Should create patterns at center when no position specified."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(9, 9)  # 9x9 grid, center at (4,4)

        success = PatternLibrary.create_pattern("block", game)  # No x,y specified
        assert success == True

        # Should be created near center
        alive_count = sum(
            1 for y in range(9) for x in range(9) if game.grid.get_cell(x, y)
        )
        assert alive_count == 4  # Block has 4 cells

    def test_invalid_pattern_name(self):
        """Should handle invalid pattern names gracefully."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(5, 5)

        success = PatternLibrary.create_pattern("invalid_pattern", game, 2, 2)
        assert success == False

        # Grid should remain empty
        alive_count = sum(
            1 for y in range(5) for x in range(5) if game.grid.get_cell(x, y)
        )
        assert alive_count == 0

    def test_blinker_oscillation_with_library(self):
        """Should verify library Blinker oscillates correctly."""
        from game_of_life.patterns import PatternLibrary
        from game_of_life.game_engine import GameOfLife

        game = GameOfLife(7, 7)
        PatternLibrary.create_blinker(game, 3, 3)

        # Generation 0: horizontal
        gen0_horizontal = [(2, 3), (3, 3), (4, 3)]
        for x, y in gen0_horizontal:
            assert game.grid.get_cell(x, y) == True

        # Generation 1: should be vertical
        game.next_generation()
        gen1_vertical = [(3, 2), (3, 3), (3, 4)]
        for x, y in gen1_vertical:
            assert game.grid.get_cell(x, y) == True

        # Population should remain 3
        alive_count = sum(
            1 for y in range(7) for x in range(7) if game.grid.get_cell(x, y)
        )
        assert alive_count == 3
