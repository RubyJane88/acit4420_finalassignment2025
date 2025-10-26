#!/usr/bin/env python3
"""
Famous Patterns Demo for Conway's Game of Life
Demonstrates all patterns in the library with their unique behaviors.
"""

import time
from game_of_life.game_engine import GameOfLife
from game_of_life.visualizer import Visualizer
from game_of_life.patterns import PatternLibrary


def demo_pattern(pattern_name: str, generations: int = 6, grid_size: tuple = (9, 9)):
    """
    Demonstrate a specific pattern with animation.
    
    Args:
        pattern_name: Name of the pattern to demonstrate
        generations: Number of generations to show
        grid_size: Size of the grid (width, height)
    """
    width, height = grid_size
    game = GameOfLife(width, height)
    visualizer = Visualizer()
    
    # Get pattern info
    patterns_info = PatternLibrary.get_pattern_info()
    if pattern_name not in patterns_info:
        print(f"❌ Pattern '{pattern_name}' not found!")
        return
    
    info = patterns_info[pattern_name]
    
    # Create the pattern
    success = PatternLibrary.create_pattern(pattern_name, game)
    if not success:
        print(f"❌ Failed to create pattern '{pattern_name}'!")
        return
    
    print(f"\n{info['emoji']} {info['name'].upper()} PATTERN DEMO")
    print("=" * 50)
    print(f"Type: {info['type'].title()}")
    print(f"Period: {info['period']}")
    print(f"Description: {info['description']}")
    print("=" * 50)
    
    try:
        for generation in range(generations):
            visualizer.print_grid(game.grid, generation=generation, clear=True)
            
            # Show pattern-specific information
            if info['type'] == 'oscillator':
                print(f"🔄 Oscillator (Period {info['period']})")
            elif info['type'] == 'still_life':
                print("⚡ Still Life (Should never change)")
            elif info['type'] == 'spaceship':
                print("🚀 Spaceship (Traveling pattern)")
            
            print(f"⏱️  Generation {generation}")
            
            if generation < generations - 1:
                print("⏳ Evolving... (Press Ctrl+C to skip)")
                time.sleep(1.5)
                game.next_generation()
        
        print(f"\n✅ {info['name']} demo complete!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  {info['name']} demo stopped early")


def demo_all_patterns():
    """Demonstrate all patterns in the library."""
    patterns_info = PatternLibrary.get_pattern_info()
    
    print("🎮 CONWAY'S GAME OF LIFE - FAMOUS PATTERNS SHOWCASE")
    print("=" * 60)
    print("🎬 Showcasing all famous patterns in the library")
    print("Press Ctrl+C at any time to skip to next pattern\n")
    
    for i, (pattern_name, info) in enumerate(patterns_info.items(), 1):
        print(f"\n📍 Pattern {i}/{len(patterns_info)}: {info['name']}")
        input("Press Enter to start demo (or Ctrl+C to exit)...")
        
        # Determine appropriate grid size and generations
        if pattern_name == "glider":
            grid_size = (12, 12)  # Larger for spaceship movement
            generations = 8
        elif pattern_name in ["block", "beehive", "loaf"]:
            grid_size = (7, 7)    # Smaller for still lifes
            generations = 3       # Fewer generations (they don't change)
        else:
            grid_size = (9, 9)    # Standard size
            generations = 6
        
        demo_pattern(pattern_name, generations, grid_size)
        
        if i < len(patterns_info):
            print("\n" + "⏭️ " * 20)
    
    print("\n🎉 All patterns demonstrated!")
    print("🎓 You've seen the most famous Conway's Game of Life patterns!")


def quick_pattern_showcase():
    """Show all patterns side by side without animation."""
    patterns_info = PatternLibrary.get_pattern_info()
    visualizer = Visualizer()
    
    print("⚡ QUICK PATTERN SHOWCASE")
    print("=" * 40)
    
    for pattern_name, info in patterns_info.items():
        game = GameOfLife(7, 7)
        PatternLibrary.create_pattern(pattern_name, game)
        
        print(f"\n{info['emoji']} {info['name']} ({info['type']})")
        print("-" * 30)
        print(visualizer.display_grid(game.grid, generation=0))


def interactive_pattern_explorer():
    """Interactive explorer for individual patterns."""
    patterns_info = PatternLibrary.get_pattern_info()
    
    while True:
        print("\n🔍 INTERACTIVE PATTERN EXPLORER")
        print("=" * 40)
        
        for i, (pattern_name, info) in enumerate(patterns_info.items(), 1):
            print(f"{i}. {info['emoji']} {info['name']} ({info['type']})")
        
        print(f"{len(patterns_info) + 1}. 🚪 Exit")
        print("=" * 40)
        
        try:
            choice = int(input("Select pattern to explore: "))
            
            if choice == len(patterns_info) + 1:
                print("👋 Thanks for exploring patterns!")
                break
            elif 1 <= choice <= len(patterns_info):
                pattern_name = list(patterns_info.keys())[choice - 1]
                generations = int(input("Enter number of generations (1-20): ") or "6")
                demo_pattern(pattern_name, min(max(generations, 1), 20))
            else:
                print("❌ Invalid choice!")
                
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Thanks for exploring patterns!")
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "--quick":
            quick_pattern_showcase()
        elif command == "--interactive":
            interactive_pattern_explorer()
        elif command in PatternLibrary.get_pattern_info():
            demo_pattern(command)
        else:
            print(f"❌ Unknown command: {command}")
            print("Available options: --quick, --interactive, or pattern name")
    else:
        print("Starting full demo in 3 seconds...")
        print("(Use --quick for static showcase, --interactive for explorer)")
        time.sleep(3)
        demo_all_patterns()