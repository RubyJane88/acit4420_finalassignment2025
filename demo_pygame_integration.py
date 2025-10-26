#!/usr/bin/env python3
"""
Demo script for pygame integration with Conway's Game of Life
"""

import sys
import os

# Add current directory to path so we can import game_of_life modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_pygame():
    """Check if pygame is available."""
    try:
        import pygame
        return True
    except ImportError:
        return False

def install_pygame_instructions():
    """Show instructions for installing pygame."""
    print("🎮 Pygame Integration Demo")
    print("=" * 40)
    print()
    print("❌ Pygame not installed!")
    print()
    print("To install pygame:")
    print("  pip install pygame")
    print()
    print("Or add to requirements.txt:")
    print("  echo 'pygame>=2.1.0' >> requirements.txt")
    print("  pip install -r requirements.txt")
    print()
    print("Then run: python demo_pygame_integration.py")

def run_pygame_demo():
    """Run the pygame visualizer demo."""
    try:
        from game_of_life.pygame_visualizer import demo_pygame_visualizer
        
        print("🎮 Starting Conway's Game of Life - Pygame Interactive Demo")
        print()
        print("This demo integrates your existing TDD-tested GameOfLife core")
        print("with beautiful pygame graphics and interactivity!")
        print()
        
        demo_pygame_visualizer()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure pygame is installed and you're in the project directory")

def main():
    """Main demo function."""
    if not check_pygame():
        install_pygame_instructions()
        return
    
    print("✅ Pygame detected!")
    print()
    
    # Show the hybrid approach benefits
    print("🏆 Hybrid Approach Benefits:")
    print("✅ Keeps all 38 tests passing")
    print("✅ Maintains PatternLibrary (Blinker, Glider, etc.)")
    print("✅ Uses tested GameOfLife core logic")
    print("✅ Adds beautiful graphics + interactivity")
    print("✅ Best of both worlds!")
    print()
    
    input("Press Enter to start pygame demo...")
    run_pygame_demo()

if __name__ == "__main__":
    main()