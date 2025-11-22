#!/usr/bin/env python3
"""
Test script for File I/O functionality.
Demonstrates reading deliveries, processing, and writing output files.
"""

from courier_optimizer.courier_optimizer import CourierOptimizer
import os


def test_file_io():
    """Test complete File I/O workflow."""
    print("\n" + "=" * 60)
    print("  FILE I/O TEST - CourierOptimizer")
    print("=" * 60 + "\n")

    optimizer = CourierOptimizer()

    # Define file paths
    input_file = "data/deliveries.csv"
    output_dir = "output"
    route_file = os.path.join(output_dir, "route.csv")
    rejected_file = os.path.join(output_dir, "rejected.csv")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print("📁 Step 1: Reading deliveries from CSV...")
    print(f"   Input file: {input_file}\n")

    try:
        # Read CSV file
        data = optimizer.read_deliveries_csv(input_file)
        print(f"✅ Successfully read {len(data)} deliveries from CSV\n")

        # Process data (validate)
        print("🔍 Step 2: Validating deliveries...")
        result = optimizer.process_csv_data(data)

        valid_deliveries = result["valid_deliveries"]
        invalid_deliveries = result["invalid_deliveries"]

        print(f"   ✅ Valid deliveries: {len(valid_deliveries)}")
        print(f"   ❌ Invalid deliveries: {len(invalid_deliveries)}\n")

        # Write rejected deliveries
        print("📝 Step 3: Writing rejected deliveries...")
        optimizer.write_rejected_csv(invalid_deliveries, rejected_file)

        if valid_deliveries:
            # Optimize route
            print("\n🎯 Step 4: Optimizing route...")
            transport_mode = "CAR"
            criteria = "FASTEST"

            route = optimizer.optimize_route(valid_deliveries, transport_mode, criteria)
            print(f"   Optimized {len(route)} deliveries")
            print(f"   Transport mode: {transport_mode}")
            print(f"   Criteria: {criteria}\n")

            # Calculate route metrics
            print("📊 Step 5: Calculating route metrics...")
            metrics = optimizer.calculate_route_metrics(route, transport_mode)

            # Write route to CSV
            print("\n💾 Step 6: Writing optimized route to CSV...")
            optimizer.write_route_csv(route, metrics, route_file, transport_mode)

            print("\n" + "=" * 60)
            print("  ✅ FILE I/O TEST COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"\n📂 Output files created:")
            print(f"   • {route_file}")
            print(f"   • {rejected_file}")
            print(f"\n💡 You can now open these CSV files to see the results!\n")
        else:
            print("\n⚠️  No valid deliveries to process!")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"   Make sure {input_file} exists!")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    test_file_io()
