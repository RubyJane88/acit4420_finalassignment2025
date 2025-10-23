"""
Tests for Conway's Game of Life - Grid Module
Following TDD approach: Write tests first, then implement features.
"""

import pytest
from game_of_life.grid import Grid


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


