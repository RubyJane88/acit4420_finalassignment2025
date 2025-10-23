"""
Conway's Game of Life - Grid Module
Manages the 2D grid data structure for the cellular automaton.
"""

import random
from typing import List, Tuple


class Grid:
    """
    Represents a 2D grid for Conway's Game of Life.
    
    Each cell can be alive (True) or dead (False).
    The grid uses a 2D list where grid[y][x] accesses the cell at position (x, y).
    """
    
    def __init__(self, width: int, height: int):
        """
        Initialize a grid with all cells dead.
        
        Args:
            width: Number of columns
            height: Number of rows
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers")
        
        self.width = width
        self.height = height
        self.cells = [[False for _ in range(width)] for _ in range(height)]
    
    def set_cell(self, x: int, y: int, alive: bool) -> None:
        """
        Set the state of a specific cell.
        
        Args:
            x: Column index (0 to width-1)
            y: Row index (0 to height-1)
            alive: True for alive, False for dead
        
        Raises:
            IndexError: If coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Cell ({x}, {y}) is out of bounds for grid {self.width}x{self.height}")
        
        self.cells[y][x] = alive
    
    def get_cell(self, x: int, y: int) -> bool:
        """
        Get the state of a specific cell.
        
        Args:
            x: Column index (0 to width-1)
            y: Row index (0 to height-1)
        
        Returns:
            True if cell is alive, False if dead
        
        Raises:
            IndexError: If coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Cell ({x}, {y}) is out of bounds for grid {self.width}x{self.height}")
        
        return self.cells[y][x]
    
    def count_neighbors(self, x: int, y: int) -> int:
        """
        Count living neighbors for a cell (maximum 8).
        
        Uses a toroidal topology - edges wrap around (like Pac-Man).
        
        Args:
            x: Column index
            y: Row index
        
        Returns:
            Number of living neighbors (0-8)
        """
        count = 0
        
        # Check all 8 surrounding cells
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                # Skip the cell itself
                if dx == 0 and dy == 0:
                    continue
                
                # Wrap around edges (toroidal grid)
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                
                if self.cells[ny][nx]:
                    count += 1
        
        return count
    
    def get_living_cells(self) -> int:
        """
        Count total number of living cells in the grid.
        
        Returns:
            Number of alive cells
        """
        count = 0
        for row in self.cells:
            count += sum(1 for cell in row if cell)
        return count
    
    def clear(self) -> None:
        """Reset all cells to dead state."""
        self.cells = [[False for _ in range(self.width)] for _ in range(self.height)]
    
    def randomize(self, density: float = 0.3) -> None:
        """
        Fill grid with random pattern.
        
        Args:
            density: Probability (0.0 to 1.0) that each cell is alive
        
        Raises:
            ValueError: If density is not between 0 and 1
        """
        if not (0.0 <= density <= 1.0):
            raise ValueError("Density must be between 0.0 and 1.0")
        
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x] = random.random() < density
    
    def set_pattern(self, pattern: List[List[int]], offset_x: int = 0, offset_y: int = 0) -> None:
        """
        Place a pattern on the grid at specified offset.
        
        Args:
            pattern: 2D list where 1=alive, 0=dead
            offset_x: X coordinate to place pattern (top-left)
            offset_y: Y coordinate to place pattern (top-left)
        
        Example:
            glider = [
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ]
            grid.set_pattern(glider, 5, 5)
        """
        for py, row in enumerate(pattern):
            for px, cell in enumerate(row):
                x = offset_x + px
                y = offset_y + py
                
                # Only set if within bounds
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.cells[y][x] = bool(cell)
    
    def copy(self) -> 'Grid':
        """
        Create a deep copy of the grid.
        
        Returns:
            New Grid instance with same state
        """
        new_grid = Grid(self.width, self.height)
        new_grid.cells = [row[:] for row in self.cells]
        return new_grid
    
    def __str__(self) -> str:
        """
        String representation for debugging.
        
        Returns:
            Multi-line string showing grid state (● for alive, ○ for dead)
        """
        lines = []
        for row in self.cells:
            line = ''.join('●' if cell else '○' for cell in row)
            lines.append(line)
        return '\n'.join(lines)
    
    def __eq__(self, other) -> bool:
        """
        Check if two grids are equal.
        
        Useful for detecting stable states.
        """
        if not isinstance(other, Grid):
            return False
        return (self.width == other.width and 
                self.height == other.height and 
                self.cells == other.cells)
