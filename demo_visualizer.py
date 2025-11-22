#!/usr/bin/env python3
"""
Quick demo of the Conway's Game of Life Visualizer
"""

from game_of_life.grid import Grid
from game_of_life.game_engine import GameOfLife
from game_of_life.visualizer import Visualizer


def demo_blinker_pattern():
    """Demonstrate the famous Blinker pattern visualization."""
    print("=== Conway's Game of Life - Blinker Pattern Demo ===\n")

    # Create 5x5 grid and game engine
    game = GameOfLife(5, 5)
    visualizer = Visualizer()

    # Set up Blinker pattern (horizontal)
    print("Setting up Blinker pattern...")
    game.grid.set_cell(1, 2, True)
    game.grid.set_cell(2, 2, True)
    game.grid.set_cell(3, 2, True)

    # Show initial state
    print("\nGeneration 0 (Horizontal Blinker):")
    print(visualizer.display_grid(game.grid, generation=0))

    # Evolution to next generation
    game.next_generation()
    print("\nGeneration 1 (Vertical Blinker):")
    print(visualizer.display_grid(game.grid, generation=1))

    # Evolution back
    game.next_generation()
    print("\nGeneration 2 (Horizontal Blinker - Full Oscillation):")
    print(visualizer.display_grid(game.grid, generation=2))


if __name__ == "__main__":
    demo_blinker_pattern()
