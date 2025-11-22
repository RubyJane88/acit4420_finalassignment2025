"""
Pygame Visualizer for Conway's Game of Life
Integrates with existing GameOfLife core while providing beautiful graphics and interactivity.
"""

import pygame
from typing import Optional, Tuple
from .game_engine import GameOfLife
from .patterns import PatternLibrary


class PygameVisualizer:
    """
    Interactive pygame visualizer for Conway's Game of Life.

    Features:
    - Beautiful graphics with colored cells
    - Mouse click to toggle cells
    - Keyboard controls (space=play/pause, c=clear, r=reset)
    - Pattern loading from PatternLibrary
    - Real-time generation counter and population display
    """

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    DARK_GREY = (64, 64, 64)
    GREEN = (0, 200, 0)
    YELLOW = (255, 255, 0)
    BLUE = (100, 150, 255)
    RED = (255, 100, 100)

    def __init__(
        self,
        grid_width: int = 40,
        grid_height: int = 30,
        tile_size: int = 20,
        fps: int = 5,
    ):
        """
        Initialize pygame visualizer.

        Args:
            grid_width: Number of cells horizontally
            grid_height: Number of cells vertically
            tile_size: Size of each cell in pixels
            fps: Target frames per second
        """
        pygame.init()

        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_size = tile_size
        self.fps = fps

        # Screen setup
        self.width = grid_width * tile_size
        self.height = grid_height * tile_size + 60  # Extra space for UI
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Conway's Game of Life - Interactive")

        # Game state
        self.game = GameOfLife(grid_width, grid_height)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.generation_counter = 0

        # Font for UI text
        self.font = pygame.font.Font(None, 24)

    def run(self) -> None:
        """Main game loop with interactive controls."""
        print("🎮 Conway's Game of Life - Pygame Interactive")
        print("Controls:")
        print("  Mouse: Click to toggle cells")
        print("  SPACE: Play/Pause simulation")
        print("  C: Clear grid")
        print("  R: Reset to initial state")
        print("  B: Load Blinker pattern")
        print("  G: Load Glider pattern")
        print("  ESC: Exit")
        print()

        # Store initial state for reset
        initial_state = self._save_grid_state()

        while self.running:
            self._handle_events(initial_state)

            if self.playing:
                self.game.next_generation()
                self.generation_counter += 1
                # Print debug info for blinker testing
                if self.generation_counter <= 10:
                    alive_count = self._count_alive_cells()
                    print(f"Gen {self.generation_counter}: {alive_count} alive cells")

            self._draw()
            self.clock.tick(self.fps)

        pygame.quit()

    def _handle_events(self, initial_state: list) -> None:
        """Handle pygame events (mouse, keyboard)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.playing = not self.playing
                    status = "Playing" if self.playing else "Paused"
                    pygame.display.set_caption(f"Conway's Game of Life - {status}")

                elif event.key == pygame.K_c:
                    self._clear_grid()

                elif event.key == pygame.K_r:
                    self._restore_grid_state(initial_state)

                elif event.key == pygame.K_b:
                    self._load_pattern("blinker")

                elif event.key == pygame.K_g:
                    self._load_pattern("glider")

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def _handle_mouse_click(self, pos: Tuple[int, int]) -> None:
        """Toggle cell state on mouse click."""
        mouse_x, mouse_y = pos

        # Check if click is in grid area (not UI area)
        if mouse_y >= self.grid_height * self.tile_size:
            return

        grid_x = mouse_x // self.tile_size
        grid_y = mouse_y // self.tile_size

        # Bounds check
        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            current_state = self.game.grid.get_cell(grid_x, grid_y)
            self.game.grid.set_cell(grid_x, grid_y, not current_state)

    def _draw(self) -> None:
        """Draw the complete game state."""
        self.screen.fill(self.WHITE)

        self._draw_grid()
        self._draw_cells()
        self._draw_ui()

        pygame.display.flip()

    def _draw_grid(self) -> None:
        """Draw grid lines."""
        # Vertical lines
        for x in range(self.grid_width + 1):
            start_pos = (x * self.tile_size, 0)
            end_pos = (x * self.tile_size, self.grid_height * self.tile_size)
            pygame.draw.line(self.screen, self.GREY, start_pos, end_pos, 1)

        # Horizontal lines
        for y in range(self.grid_height + 1):
            start_pos = (0, y * self.tile_size)
            end_pos = (self.grid_width * self.tile_size, y * self.tile_size)
            pygame.draw.line(self.screen, self.GREY, start_pos, end_pos, 1)

    def _draw_cells(self) -> None:
        """Draw alive cells as colored rectangles."""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.game.grid.get_cell(x, y):
                    rect = pygame.Rect(
                        x * self.tile_size + 1,
                        y * self.tile_size + 1,
                        self.tile_size - 2,
                        self.tile_size - 2,
                    )
                    pygame.draw.rect(self.screen, self.GREEN, rect)

    def _draw_ui(self) -> None:
        """Draw UI information (generation, population, controls)."""
        ui_y = self.grid_height * self.tile_size + 5

        # Generation counter
        generation_text = f"Generation: {self.generation_counter}"
        gen_surface = self.font.render(generation_text, True, self.BLACK)
        self.screen.blit(gen_surface, (10, ui_y))

        # Population count
        alive_count = self._count_alive_cells()
        total_cells = self.grid_width * self.grid_height
        pop_text = f"Population: {alive_count}/{total_cells}"
        pop_surface = self.font.render(pop_text, True, self.BLACK)
        self.screen.blit(pop_surface, (200, ui_y))

        # Status
        status = "Playing" if self.playing else "Paused"
        status_color = self.GREEN if self.playing else self.RED
        status_surface = self.font.render(f"Status: {status}", True, status_color)
        self.screen.blit(status_surface, (400, ui_y))

        # Controls hint
        controls_text = (
            "SPACE: Play/Pause | C: Clear | B: Blinker | G: Glider | ESC: Exit"
        )
        controls_surface = self.font.render(controls_text, True, self.DARK_GREY)
        self.screen.blit(controls_surface, (10, ui_y + 25))

    def _count_alive_cells(self) -> int:
        """Count total alive cells in grid."""
        count = 0
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.game.grid.get_cell(x, y):
                    count += 1
        return count

    def _clear_grid(self) -> None:
        """Clear all cells and reset generation counter."""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.game.grid.set_cell(x, y, False)
        self.generation_counter = 0
        self.playing = False

    def _save_grid_state(self) -> list:
        """Save current grid state for reset functionality."""
        state = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                row.append(self.game.grid.get_cell(x, y))
            state.append(row)
        return state

    def _restore_grid_state(self, state: list) -> None:
        """Restore grid to saved state."""
        for y in range(len(state)):
            for x in range(len(state[0])):
                self.game.grid.set_cell(x, y, state[y][x])
        self.generation_counter = 0
        self.playing = False

    def _load_pattern(self, pattern_name: str) -> None:
        """Load a pattern from PatternLibrary."""
        self._clear_grid()

        # Place pattern in center of grid
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2

        success = PatternLibrary.create_pattern(
            pattern_name, self.game, center_x, center_y
        )

        if success:
            pattern_info = PatternLibrary.get_pattern_info().get(pattern_name, {})
            print(
                f"✨ Loaded {pattern_info.get('name', pattern_name)} pattern at ({center_x}, {center_y})"
            )
            # Show initial state
            alive_count = self._count_alive_cells()
            print(f"Initial state: {alive_count} alive cells")
        else:
            print(f"❌ Failed to load pattern: {pattern_name}")

    def load_custom_pattern(self, pattern_coords: list) -> None:
        """
        Load custom pattern from coordinate list.

        Args:
            pattern_coords: List of (x, y) tuples for alive cells
        """
        self._clear_grid()

        for x, y in pattern_coords:
            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                self.game.grid.set_cell(x, y, True)


def demo_pygame_visualizer():
    """Demo function to showcase pygame visualizer."""
    print("🎬 Starting Conway's Game of Life - Pygame Demo")
    print()

    # Create visualizer with reasonable grid size
    viz = PygameVisualizer(grid_width=50, grid_height=40, tile_size=15, fps=8)

    # Load initial Blinker pattern for demo
    viz._load_pattern("blinker")

    # Run interactive simulation
    viz.run()


if __name__ == "__main__":
    demo_pygame_visualizer()
