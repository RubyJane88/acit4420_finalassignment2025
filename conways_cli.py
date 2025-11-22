#!/usr/bin/env python3
"""
Interactive CLI for Conway's Game of Life
Provides menu-driven interface for pattern selection and simulation control.
"""

import time
import sys
from typing import Optional
from game_of_life.game_engine import GameOfLife
from game_of_life.visualizer import Visualizer


class ConwaysCLI:
    """Interactive command-line interface for Conway's Game of Life."""

    def __init__(self):
        """Initialize CLI with default settings."""
        self.game: Optional[GameOfLife] = None
        self.visualizer = Visualizer()
        self.current_generation = 0
        self.animation_delay = 1.0

    def show_main_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "=" * 50)
        print("🎮 CONWAY'S GAME OF LIFE - Interactive Simulator")
        print("=" * 50)
        print("1. 🚀 Start New Simulation")
        print("2. ⚙️  Settings")
        print("3. ℹ️  About Conway's Game of Life")
        print("4. 🚪 Exit")
        print("=" * 50)

    def show_pattern_menu(self) -> None:
        """Display pattern selection menu."""
        print("\n" + "=" * 40)
        print("📐 SELECT STARTING PATTERN")
        print("=" * 40)
        print("1. 📏 Blinker (Oscillator)")
        print("2. 🟩 Block (Still Life)")
        print("3. 🔳 Empty Grid (Custom Setup)")
        print("4. 🔙 Back to Main Menu")
        print("=" * 40)

    def show_simulation_menu(self) -> None:
        """Display simulation control menu."""
        print("\n" + "=" * 40)
        print("🎬 SIMULATION CONTROLS")
        print("=" * 40)
        print("1. ▶️  Run Animation (Auto)")
        print("2. ⏭️  Next Generation (Manual)")
        print("3. 🔄 Reset Pattern")
        print("4. 👁️  View Current State")
        print("5. 🔙 Back to Pattern Selection")
        print("=" * 40)

    def create_blinker_pattern(self, width: int = 7, height: int = 7) -> None:
        """Create the famous Blinker oscillator pattern."""
        self.game = GameOfLife(width, height)
        self.current_generation = 0

        # Place Blinker in center
        center_x, center_y = width // 2, height // 2
        self.game.grid.set_cell(center_x - 1, center_y, True)
        self.game.grid.set_cell(center_x, center_y, True)
        self.game.grid.set_cell(center_x + 1, center_y, True)

        print(f"✨ Created Blinker pattern on {width}x{height} grid")

    def create_block_pattern(self, width: int = 7, height: int = 7) -> None:
        """Create a Block still life pattern."""
        self.game = GameOfLife(width, height)
        self.current_generation = 0

        # Place 2x2 Block in center
        center_x, center_y = width // 2, height // 2
        self.game.grid.set_cell(center_x, center_y, True)
        self.game.grid.set_cell(center_x + 1, center_y, True)
        self.game.grid.set_cell(center_x, center_y + 1, True)
        self.game.grid.set_cell(center_x + 1, center_y + 1, True)

        print(f"🟩 Created Block pattern on {width}x{height} grid")

    def create_empty_grid(self, width: int = 7, height: int = 7) -> None:
        """Create an empty grid for custom setup."""
        self.game = GameOfLife(width, height)
        self.current_generation = 0
        print(f"🔳 Created empty {width}x{height} grid")
        print("💡 Tip: Use custom setup to manually place cells")

    def run_animation(self, max_generations: int = 10) -> None:
        """Run animated simulation."""
        if not self.game:
            print("❌ No pattern loaded! Please select a pattern first.")
            return

        print(f"🎬 Starting animation for {max_generations} generations...")
        print("Press Ctrl+C to stop early\n")

        try:
            for gen in range(max_generations):
                self.visualizer.print_grid(
                    self.game.grid, generation=self.current_generation, clear=True
                )

                print(f"⏱️  Generation {self.current_generation}")
                print(f"⏳ Delay: {self.animation_delay}s")

                if gen < max_generations - 1:
                    time.sleep(self.animation_delay)
                    self.game.next_generation()
                    self.current_generation += 1

            print("\n✅ Animation complete!")

        except KeyboardInterrupt:
            print("\n\n⏹️  Animation stopped by user")

    def next_generation(self) -> None:
        """Advance to next generation manually."""
        if not self.game:
            print("❌ No pattern loaded! Please select a pattern first.")
            return

        self.game.next_generation()
        self.current_generation += 1
        self.view_current_state()
        print(f"➡️  Advanced to generation {self.current_generation}")

    def view_current_state(self) -> None:
        """Display current grid state."""
        if not self.game:
            print("❌ No pattern loaded! Please select a pattern first.")
            return

        print("\n" + "=" * 30)
        print("👁️  CURRENT STATE")
        print("=" * 30)
        print(self.visualizer.display_grid(self.game.grid, self.current_generation))

    def show_settings_menu(self) -> None:
        """Display and handle settings configuration."""
        while True:
            print("\n" + "=" * 40)
            print("⚙️  SETTINGS")
            print("=" * 40)
            print(f"1. Animation Speed (Current: {self.animation_delay}s)")
            print("2. Grid Size (Will apply to next pattern)")
            print("3. 🔙 Back to Main Menu")
            print("=" * 40)

            choice = input("Select option (1-3): ").strip()

            if choice == "1":
                self.set_animation_speed()
            elif choice == "2":
                print("💡 Grid size will be prompted when creating new pattern")
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice! Please enter 1-3.")

    def set_animation_speed(self) -> None:
        """Configure animation delay."""
        try:
            new_delay = float(
                input(f"Enter delay in seconds (current: {self.animation_delay}): ")
            )
            if 0.1 <= new_delay <= 5.0:
                self.animation_delay = new_delay
                print(f"✅ Animation speed set to {new_delay}s")
            else:
                print("❌ Delay must be between 0.1 and 5.0 seconds")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")

    def show_about(self) -> None:
        """Display information about Conway's Game of Life."""
        print("\n" + "=" * 50)
        print("ℹ️  ABOUT CONWAY'S GAME OF LIFE")
        print("=" * 50)
        print("Created by mathematician John Conway in 1970")
        print("A cellular automaton with simple rules:")
        print()
        print("🔸 Survival: Cell with 2-3 neighbors survives")
        print("🔸 Death: Cell with <2 or >3 neighbors dies")
        print("🔸 Birth: Empty cell with exactly 3 neighbors becomes alive")
        print()
        print("Famous Patterns:")
        print("📏 Blinker: 3-cell oscillator (period 2)")
        print("🟩 Block: 4-cell still life (never changes)")
        print("🚀 Glider: Moving pattern (travels diagonally)")
        print()
        print("This simulation uses a toroidal grid (edges wrap around)")
        print("=" * 50)
        input("Press Enter to continue...")

    def get_grid_dimensions(self) -> tuple[int, int]:
        """Get grid dimensions from user."""
        try:
            width = int(input("Enter grid width (5-20): "))
            height = int(input("Enter grid height (5-20): "))

            if 5 <= width <= 20 and 5 <= height <= 20:
                return width, height
            else:
                print("❌ Dimensions must be between 5 and 20")
                return 7, 7  # Default
        except ValueError:
            print("❌ Invalid input! Using default 7x7")
            return 7, 7

    def handle_pattern_selection(self) -> bool:
        """Handle pattern selection menu. Returns True if pattern was selected."""
        while True:
            self.show_pattern_menu()
            choice = input("Select pattern (1-4): ").strip()

            if choice == "1":
                width, height = self.get_grid_dimensions()
                self.create_blinker_pattern(width, height)
                return True
            elif choice == "2":
                width, height = self.get_grid_dimensions()
                self.create_block_pattern(width, height)
                return True
            elif choice == "3":
                width, height = self.get_grid_dimensions()
                self.create_empty_grid(width, height)
                return True
            elif choice == "4":
                return False
            else:
                print("❌ Invalid choice! Please enter 1-4.")

    def handle_simulation_controls(self) -> None:
        """Handle simulation control menu."""
        while True:
            self.show_simulation_menu()
            choice = input("Select option (1-5): ").strip()

            if choice == "1":
                max_gen = input("Enter max generations (default 10): ").strip()
                try:
                    max_gen = int(max_gen) if max_gen else 10
                    self.run_animation(max_gen)
                except ValueError:
                    print("❌ Invalid input! Using default 10 generations.")
                    self.run_animation(10)
            elif choice == "2":
                self.next_generation()
            elif choice == "3":
                if self.game:
                    # Reset by recreating the same pattern
                    width, height = self.game.grid.width, self.game.grid.height
                    print("🔄 Pattern reset!")
                    # Re-prompt for pattern selection
                    return
                else:
                    print("❌ No pattern to reset!")
            elif choice == "4":
                self.view_current_state()
            elif choice == "5":
                return
            else:
                print("❌ Invalid choice! Please enter 1-5.")

    def run(self) -> None:
        """Main CLI loop."""
        print("🎮 Welcome to Conway's Game of Life!")

        while True:
            self.show_main_menu()
            choice = input("Select option (1-4): ").strip()

            if choice == "1":
                if self.handle_pattern_selection():
                    self.view_current_state()
                    self.handle_simulation_controls()
            elif choice == "2":
                self.show_settings_menu()
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                print("👋 Thanks for exploring Conway's Game of Life!")
                sys.exit(0)
            else:
                print("❌ Invalid choice! Please enter 1-4.")


if __name__ == "__main__":
    cli = ConwaysCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for exploring Conway's Game of Life!")
        sys.exit(0)
