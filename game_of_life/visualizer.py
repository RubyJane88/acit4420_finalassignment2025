"""
ASCII Visualizer for Conway's Game of Life
Provides visual display of grid state with generation counter and statistics.
"""

import os
from typing import Optional
from .grid import Grid


class Visualizer:
    """
    ASCII-based visualizer for Conway's Game of Life.

    Displays the grid using:
    - ● (filled circle) for alive cells
    - ○ (empty circle) for dead cells

    Includes generation counter and population statistics.
    """

    ALIVE_SYMBOL = "●"
    DEAD_SYMBOL = "○"

    def __init__(self):
        """Initialize the visualizer."""
        pass

    def display_grid(self, grid: Grid, generation: int = 0) -> str:
        """
        Generate ASCII representation of the grid with statistics.

        Args:
            grid: The Grid instance to display
            generation: Current generation number

        Returns:
            String containing the formatted grid display
        """
        lines = []

        # Header with generation info
        lines.append(f"Generation: {generation}")
        lines.append("=" * (grid.width * 2))

        # Grid display
        for y in range(grid.height):
            row = ""
            for x in range(grid.width):
                if grid.get_cell(x, y):
                    row += self.ALIVE_SYMBOL + " "
                else:
                    row += self.DEAD_SYMBOL + " "
            lines.append(row.rstrip())  # Remove trailing space

        # Statistics
        lines.append("=" * (grid.width * 2))
        alive_count = self._count_alive_cells(grid)
        total_cells = grid.width * grid.height
        lines.append(f"Population: {alive_count} / {total_cells}")

        return "\n".join(lines)

    def clear_screen(self) -> None:
        """Clear the terminal screen for animation effect."""
        os.system("clear" if os.name == "posix" else "cls")

    def print_grid(self, grid: Grid, generation: int = 0, clear: bool = True) -> None:
        """
        Print the grid to console with optional screen clearing.

        Args:
            grid: The Grid instance to display
            generation: Current generation number
            clear: Whether to clear screen before printing
        """
        if clear:
            self.clear_screen()

        print(self.display_grid(grid, generation))

    def _count_alive_cells(self, grid: Grid) -> int:
        """
        Count the number of alive cells in the grid.

        Args:
            grid: The Grid instance to count

        Returns:
            Number of alive cells
        """
        count = 0
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.get_cell(x, y):
                    count += 1
        return count
