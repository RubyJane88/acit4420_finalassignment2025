#!/usr/bin/env python3
"""
CLI Interface for CourierOptimizer - Iteration 4
Connecting to CourierOptimizer class to actually process deliveries.
"""

from courier_optimizer.courier_optimizer import CourierOptimizer
from courier_optimizer.logger import get_logger, timer
import os


def display_main_menu():
    """Display the main menu options."""
    print("\n" + "=" * 60)
    print("  COURIER OPTIMIZER - Route Planning System")
    print("=" * 60)
    print("\nWhat would you like to do?")
    print("  1. Optimize delivery route")
    print("  2. Exit")
    print()


def get_user_choice():
    """Get user's menu choice."""
    choice = input("Enter your choice (1-2): ")
    return choice


def select_transport_mode():
    """Let user select transport mode."""
    print("\n" + "-" * 60)
    print("  SELECT TRANSPORT MODE")
    print("-" * 60)
    print("\n🚗 Available transport modes:")
    print("  1. CAR     - Fast (50 km/h), Costs 4 NOK/km, 120g CO2/km")
    print("  2. BICYCLE - Medium (15 km/h), Free, Zero emissions")
    print("  3. WALKING - Slow (5 km/h), Free, Zero emissions")
    print()

    # Loop until valid input
    while True:
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            return "CAR"
        elif choice == "2":
            return "BICYCLE"
        elif choice == "3":
            return "WALKING"
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")


def select_criteria():
    """Let user select optimization criteria."""
    print("\n" + "-" * 60)
    print("  SELECT OPTIMIZATION CRITERIA")
    print("-" * 60)
    print("\n🎯 What's most important for this delivery run?")
    print("  1. FASTEST  - Minimize total delivery time")
    print("  2. CHEAPEST - Minimize total cost")
    print("  3. GREENEST - Minimize CO2 emissions")
    print()

    # Loop until valid input
    while True:
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            return "FASTEST"
        elif choice == "2":
            return "CHEAPEST"
        elif choice == "3":
            return "GREENEST"
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")


@timer
def process_deliveries(transport_mode, criteria):
    """Process deliveries with selected transport mode and criteria."""
    print("\n" + "=" * 60)
    print("  PROCESSING DELIVERIES")
    print("=" * 60)

    optimizer = CourierOptimizer()

    # File paths
    input_file = "data/deliveries.csv"
    output_dir = "output"
    route_file = os.path.join(output_dir, "route.csv")
    rejected_file = os.path.join(output_dir, "rejected.csv")

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Step 1: Read CSV
        print(f"\n📁 Reading deliveries from {input_file}...")
        data = optimizer.read_deliveries_csv(input_file)
        print(f"✅ Loaded {len(data)} deliveries")

        # Step 2: Validate deliveries
        print("\n🔍 Validating deliveries...")
        result = optimizer.process_csv_data(data)
        valid_deliveries = result["valid_deliveries"]
        invalid_deliveries = result["invalid_deliveries"]

        print(f"   ✅ Valid: {len(valid_deliveries)}")
        print(f"   ❌ Invalid: {len(invalid_deliveries)}")

        # Save rejected deliveries
        optimizer.write_rejected_csv(invalid_deliveries, rejected_file)

        if not valid_deliveries:
            print("\n⚠️  No valid deliveries to process!")
            return

        # Step 3: Optimize route
        print(f"\n🎯 Optimizing route...")
        print(f"   Transport: {transport_mode}")
        print(f"   Criteria: {criteria}")

        route = optimizer.optimize_route(valid_deliveries, transport_mode, criteria)
        print(f"✅ Optimized {len(route)} deliveries")

        # Step 4: Calculate metrics
        print("\n📊 Calculating route metrics...")
        metrics = optimizer.calculate_route_metrics(route, transport_mode)

        # Step 5: Save route
        print("\n💾 Saving results...")
        optimizer.write_route_csv(route, metrics, route_file, transport_mode)

        # Step 6: Display summary
        print("\n" + "=" * 60)
        print("  🎉 ROUTE OPTIMIZATION COMPLETE!")
        print("=" * 60)
        print(f"\n📦 Processed {len(route)} deliveries")
        print(f"📏 Total distance: {metrics['total_distance_km']} km")
        print(
            f"⏱️  Total time: {metrics['total_time_hours']:.2f} hours ({metrics['total_time_hours']*60:.0f} minutes)"
        )
        print(f"💰 Total cost: {metrics['total_cost_nok']:.2f} NOK")
        print(
            f"🌍 Total CO2: {metrics['total_co2_grams']:.2f} g ({metrics['total_co2_grams']/1000:.2f} kg)"
        )
        print(f"\n📂 Output files:")
        print(f"   • {route_file}")
        print(f"   • {rejected_file}")

    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print(f"   Make sure '{input_file}' exists!")
    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print(f"   Type: {type(e).__name__}")


def main():
    """Main CLI loop."""
    logger = get_logger()

    logger.info("=" * 60)
    logger.info("CourierOptimizer CLI Started")
    logger.info("=" * 60)

    print("\n👋 Welcome to CourierOptimizer!")

    while True:
        display_main_menu()
        choice = get_user_choice()

        logger.info(f"User selected menu option: {choice}")

        if choice == "1":
            # Get transport mode
            transport_mode = select_transport_mode()
            logger.info(f"User selected transport mode: {transport_mode}")
            print(f"\n✅ Selected transport mode: {transport_mode}")

            # Get criteria
            criteria = select_criteria()
            logger.info(f"User selected criteria: {criteria}")
            print(f"✅ Selected criteria: {criteria}")

            # Process deliveries with selections
            process_deliveries(transport_mode, criteria)

        elif choice == "2":
            logger.info("User chose to exit")
            logger.info("CourierOptimizer CLI Ended")
            logger.info("=" * 60)

            print("\n👋 Thank you for using CourierOptimizer!")
            break
        else:
            print("\n❌ Invalid choice! Please enter 1 or 2.")


if __name__ == "__main__":
    main()
