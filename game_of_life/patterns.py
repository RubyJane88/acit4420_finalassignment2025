"""
Famous Pattern Library for Conway's Game of Life
Contains well-known patterns including oscillators, still lifes, and spaceships.
"""

from typing import List, Tuple, Dict, Any, Optional
from .grid import Grid
from .game_engine import GameOfLife


class PatternLibrary:
    """
    Library of famous Conway's Game of Life patterns.
    
    Provides easy creation of well-known patterns including:
    - Oscillators (Blinker, Toad, Beacon)
    - Still Lifes (Block, Beehive, Loaf)  
    - Spaceships (Glider)
    """
    
    @staticmethod
    def create_blinker(game: GameOfLife, center_x: int, center_y: int) -> None:
        """
        Create the famous Blinker oscillator pattern.
        
        Period: 2 generations
        Pattern: Three cells in a horizontal line that oscillates to vertical
        
        Args:
            game: GameOfLife instance to modify
            center_x, center_y: Center position for the pattern
        """
        game.grid.set_cell(center_x - 1, center_y, True)
        game.grid.set_cell(center_x, center_y, True)
        game.grid.set_cell(center_x + 1, center_y, True)
    
    @staticmethod
    def create_block(game: GameOfLife, top_left_x: int, top_left_y: int) -> None:
        """
        Create a Block still life pattern.
        
        Period: Still life (never changes)
        Pattern: 2x2 square of alive cells
        
        Args:
            game: GameOfLife instance to modify
            top_left_x, top_left_y: Top-left corner position
        """
        game.grid.set_cell(top_left_x, top_left_y, True)
        game.grid.set_cell(top_left_x + 1, top_left_y, True)
        game.grid.set_cell(top_left_x, top_left_y + 1, True)
        game.grid.set_cell(top_left_x + 1, top_left_y + 1, True)
    
    @staticmethod
    def create_beehive(game: GameOfLife, center_x: int, center_y: int) -> None:
        """
        Create a Beehive still life pattern.
        
        Period: Still life (never changes)
        Pattern: Hexagonal shape resembling a beehive
        
        Args:
            game: GameOfLife instance to modify
            center_x, center_y: Center position for the pattern
        """
        # Top row
        game.grid.set_cell(center_x, center_y - 1, True)
        game.grid.set_cell(center_x + 1, center_y - 1, True)
        
        # Middle rows
        game.grid.set_cell(center_x - 1, center_y, True)
        game.grid.set_cell(center_x + 2, center_y, True)
        
        # Bottom row  
        game.grid.set_cell(center_x, center_y + 1, True)
        game.grid.set_cell(center_x + 1, center_y + 1, True)
    
    @staticmethod
    def create_toad(game: GameOfLife, center_x: int, center_y: int) -> None:
        """
        Create a Toad oscillator pattern.
        
        Period: 2 generations
        Pattern: 6 cells that oscillate in a distinctive toad-like motion
        
        Args:
            game: GameOfLife instance to modify
            center_x, center_y: Center position for the pattern
        """
        # Top row (offset right)
        game.grid.set_cell(center_x, center_y - 1, True)
        game.grid.set_cell(center_x + 1, center_y - 1, True)
        game.grid.set_cell(center_x + 2, center_y - 1, True)
        
        # Bottom row (offset left)
        game.grid.set_cell(center_x - 1, center_y, True)
        game.grid.set_cell(center_x, center_y, True)
        game.grid.set_cell(center_x + 1, center_y, True)
    
    @staticmethod
    def create_beacon(game: GameOfLife, top_left_x: int, top_left_y: int) -> None:
        """
        Create a Beacon oscillator pattern.
        
        Period: 2 generations
        Pattern: Two blocks that flash on and off alternately
        
        Args:
            game: GameOfLife instance to modify
            top_left_x, top_left_y: Top-left corner position
        """
        # Top-left block
        game.grid.set_cell(top_left_x, top_left_y, True)
        game.grid.set_cell(top_left_x + 1, top_left_y, True)
        game.grid.set_cell(top_left_x, top_left_y + 1, True)
        
        # Bottom-right block
        game.grid.set_cell(top_left_x + 2, top_left_y + 2, True)
        game.grid.set_cell(top_left_x + 3, top_left_y + 2, True)
        game.grid.set_cell(top_left_x + 3, top_left_y + 3, True)
    
    @staticmethod
    def create_glider(game: GameOfLife, top_left_x: int, top_left_y: int) -> None:
        """
        Create the famous Glider spaceship pattern.
        
        Period: 4 generations (returns to original shape, moved diagonally)
        Pattern: 5 cells that travel diagonally across the grid
        
        Args:
            game: GameOfLife instance to modify
            top_left_x, top_left_y: Top-left position of bounding box
        """
        # Glider pattern:
        #  ○●○
        #  ○○●  
        #  ●●●
        
        game.grid.set_cell(top_left_x + 1, top_left_y, True)      # Top middle
        game.grid.set_cell(top_left_x + 2, top_left_y + 1, True)  # Right middle
        game.grid.set_cell(top_left_x, top_left_y + 2, True)      # Bottom left
        game.grid.set_cell(top_left_x + 1, top_left_y + 2, True)  # Bottom middle
        game.grid.set_cell(top_left_x + 2, top_left_y + 2, True)  # Bottom right
    
    @staticmethod
    def create_loaf(game: GameOfLife, center_x: int, center_y: int) -> None:
        """
        Create a Loaf still life pattern.
        
        Period: Still life (never changes)
        Pattern: Bread loaf-shaped stable configuration
        
        Args:
            game: GameOfLife instance to modify
            center_x, center_y: Center position for the pattern
        """
        # Loaf pattern (7 cells):
        #  ○●●○
        #  ●○○●
        #  ○●○●
        #  ○○●○
        
        # Top row
        game.grid.set_cell(center_x, center_y - 1, True)
        game.grid.set_cell(center_x + 1, center_y - 1, True)
        
        # Second row
        game.grid.set_cell(center_x - 1, center_y, True)
        game.grid.set_cell(center_x + 2, center_y, True)
        
        # Third row
        game.grid.set_cell(center_x, center_y + 1, True)
        game.grid.set_cell(center_x + 2, center_y + 1, True)
        
        # Bottom row
        game.grid.set_cell(center_x + 1, center_y + 2, True)
    
    @classmethod
    def get_pattern_info(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all available patterns.
        
        Returns:
            Dictionary with pattern names and their properties
        """
        return {
            "blinker": {
                "name": "Blinker",
                "type": "oscillator",
                "period": 2,
                "description": "Simple 3-cell oscillator",
                "emoji": "📏",
                "min_grid_size": (5, 3)
            },
            "block": {
                "name": "Block", 
                "type": "still_life",
                "period": "stable",
                "description": "2x2 square that never changes",
                "emoji": "🟩",
                "min_grid_size": (2, 2)
            },
            "beehive": {
                "name": "Beehive",
                "type": "still_life", 
                "period": "stable",
                "description": "Hexagonal stable pattern",
                "emoji": "🍯",
                "min_grid_size": (4, 3)
            },
            "toad": {
                "name": "Toad",
                "type": "oscillator",
                "period": 2,
                "description": "6-cell oscillator with toad-like motion",
                "emoji": "🐸",
                "min_grid_size": (4, 2)
            },
            "beacon": {
                "name": "Beacon",
                "type": "oscillator",
                "period": 2,
                "description": "Flashing lighthouse beacon",
                "emoji": "🚨",
                "min_grid_size": (4, 4)
            },
            "glider": {
                "name": "Glider",
                "type": "spaceship",
                "period": 4,
                "description": "Travels diagonally across grid",
                "emoji": "🚀",
                "min_grid_size": (3, 3)
            },
            "loaf": {
                "name": "Loaf",
                "type": "still_life",
                "period": "stable", 
                "description": "Bread loaf-shaped stable pattern",
                "emoji": "🍞",
                "min_grid_size": (4, 4)
            }
        }
    
    @classmethod
    def create_pattern(cls, pattern_name: str, game: GameOfLife, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        Create a pattern by name at the specified position.
        
        Args:
            pattern_name: Name of the pattern to create
            game: GameOfLife instance to modify
            x, y: Position (defaults to center of grid)
            
        Returns:
            True if pattern was created successfully, False otherwise
        """
        if x is None:
            x = game.grid.width // 2
        if y is None:
            y = game.grid.height // 2
        
        pattern_name = pattern_name.lower()
        
        try:
            if pattern_name == "blinker":
                cls.create_blinker(game, x, y)
            elif pattern_name == "block":
                cls.create_block(game, x, y)
            elif pattern_name == "beehive":
                cls.create_beehive(game, x, y)
            elif pattern_name == "toad":
                cls.create_toad(game, x, y)
            elif pattern_name == "beacon":
                cls.create_beacon(game, x, y)
            elif pattern_name == "glider":
                cls.create_glider(game, x, y)
            elif pattern_name == "loaf":
                cls.create_loaf(game, x, y)
            else:
                return False
            
            return True
            
        except Exception:
            return False