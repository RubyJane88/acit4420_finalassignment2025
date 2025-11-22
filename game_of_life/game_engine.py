"""
Conway's Game of Life - Game Engine Module
Implements the core logic for Conway's rules and generation evolution.
"""

from typing import List, Tuple
from .grid import Grid


class GameOfLife:
    """
    Main game engine for Conway's Game of Life.

    Manages the simulation state and applies Conway's 4 rules:
    1. Survival: Living cell with 2-3 neighbors stays alive
    2. Death by loneliness: Living cell with <2 neighbors dies
    3. Death by overcrowding: Living cell with >3 neighbors dies
    4. Birth: Dead cell with exactly 3 neighbors becomes alive
    """

    def __init__(self, width: int, height: int):
        """
        Initialize a new Game of Life simulation.

        Args:
            width: Grid width in cells
            height: Grid height in cells
        """
        self.grid = Grid(width, height)
        self.generation = 0
        self.width = width
        self.height = height

    def next_generation(self) -> None:
        """
        Evolve the grid to the next generation using Conway's rules.

        Creates a new grid state based on current state and Conway's rules.
        Updates the current grid and increments generation counter.
        """
        # Create new grid for next generation
        new_grid = Grid(self.width, self.height)

        # Apply Conway's rules to each cell
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.grid.count_neighbors(x, y)
                currently_alive = self.grid.get_cell(x, y)

                # Apply Conway's 4 rules
                new_state = self._apply_conway_rules(currently_alive, neighbors)
                new_grid.set_cell(x, y, new_state)

        # Update to new generation
        self.grid = new_grid
        self.generation += 1

    def _apply_conway_rules(self, is_alive: bool, neighbor_count: int) -> bool:
        """
        Apply Conway's 4 rules to determine new cell state.

        Args:
            is_alive: Current state of the cell
            neighbor_count: Number of living neighbors (0-8)

        Returns:
            True if cell should be alive in next generation, False otherwise
        """
        if is_alive:
            # Living cell rules
            if neighbor_count < 2:
                return False  # Death by loneliness
            elif neighbor_count in [2, 3]:
                return True  # Survival
            else:  # neighbor_count > 3
                return False  # Death by overcrowding
        else:
            # Dead cell rules
            if neighbor_count == 3:
                return True  # Birth
            else:
                return False  # Stay dead

    def reset(self) -> None:
        """Reset the simulation to generation 0 with empty grid."""
        self.grid.clear()
        self.generation = 0

    def get_generation(self) -> int:
        """Get current generation number."""
        return self.generation

    def get_living_cells(self) -> int:
        """Get count of living cells in current generation."""
        return self.grid.get_living_cells()
