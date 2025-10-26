#!/usr/bin/env python3
"""
Simple pygame demo focusing on blinker pattern
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_of_life.pygame_visualizer import PygameVisualizer

def blinker_demo():
    """Demo specifically for testing blinker pattern."""
    print("🔥 Blinker Pattern Demo")
    print("=" * 30)
    print()
    print("This demo will:")
    print("✅ Load a blinker pattern")
    print("✅ Start it playing immediately")
    print("✅ Show debug output in terminal")
    print()
    print("Controls:")
    print("  SPACE: pause/play")
    print("  ESC: exit")
    print()
    input("Press Enter to start...")
    
    # Create smaller grid for better visibility
    visualizer = PygameVisualizer(
        grid_width=20,
        grid_height=15, 
        tile_size=30,
        fps=3  # Very slow for clear visibility
    )
    
    # Pre-load blinker and start playing
    visualizer._load_pattern("blinker")
    visualizer.playing = True
    
    visualizer.run()

if __name__ == "__main__":
    blinker_demo()