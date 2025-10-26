#!/usr/bin/env python3
"""
Animated Conway's Game of Life Demo
Shows real-time visualization of the famous Blinker pattern oscillating.
"""

import time
from game_of_life.game_engine import GameOfLife
from game_of_life.visualizer import Visualizer


def animated_blinker_demo(generations: int = 6, delay: float = 1.5):
    """
    Demonstrate animated Blinker pattern with real-time visualization.
    
    Args:
        generations: Number of generations to simulate
        delay: Seconds to wait between generations
    """
    print("🎬 Conway's Game of Life - Animated Blinker Pattern")
    print("=" * 50)
    print("Watch the Blinker oscillate between horizontal and vertical!")
    print("Press Ctrl+C to stop early\n")
    
    # Setup
    game = GameOfLife(7, 7)  # Slightly larger for better visibility
    visualizer = Visualizer()
    
    # Create Blinker pattern in center
    center_x, center_y = 3, 3
    game.grid.set_cell(center_x - 1, center_y, True)  # Left
    game.grid.set_cell(center_x, center_y, True)      # Center  
    game.grid.set_cell(center_x + 1, center_y, True)  # Right
    
    try:
        for generation in range(generations):
            # Clear and display current state
            visualizer.print_grid(game.grid, generation=generation, clear=True)
            
            # Show pattern orientation
            if generation % 2 == 0:
                print("📏 Pattern: HORIZONTAL")
            else:
                print("📐 Pattern: VERTICAL")
            
            print(f"\n⏱️  Generation {generation}/{generations-1}")
            
            # Wait before next generation
            if generation < generations - 1:
                print("⏳ Evolving...")
                time.sleep(delay)
                game.next_generation()
            
        print("\n✅ Animation complete!")
        print("🔄 The Blinker has completed its oscillation cycle.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Animation stopped by user")
        print("👋 Thanks for watching Conway's Game of Life!")


def quick_evolution_demo():
    """Show rapid evolution without delays for testing."""
    print("⚡ Quick Evolution Demo (No Animation)\n")
    
    game = GameOfLife(5, 5)
    visualizer = Visualizer()
    
    # Blinker setup
    game.grid.set_cell(1, 2, True)
    game.grid.set_cell(2, 2, True) 
    game.grid.set_cell(3, 2, True)
    
    for gen in range(4):
        print(f"Generation {gen}:")
        print(visualizer.display_grid(game.grid, generation=gen))
        if gen < 3:
            game.next_generation()
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_evolution_demo()
    else:
        print("Starting animated demo in 3 seconds...")
        print("(Use --quick flag for rapid demo without animation)")
        time.sleep(3)
        animated_blinker_demo()