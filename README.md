# CourierOptimizer

Smart courier routing system for Oslo's delivery service NordicExpress.

## 🎯 Assignment Overview

**Course:** ACIT 4420 Scripting 2  
**Assignment:** Final Assignment 2025 - Part I  
**Development Approach:** Test-Driven Development (TDD)

## 📦 Features

- **Route Optimization:** Generate optimal routes based on:
  - Fastest total time
  - Lowest total cost
  - Lowest CO2 emissions
- **Multiple Transport Modes:** Car, Bicycle, Walking
- **Data Validation:** Robust CSV input validation with error handling
- **CLI Interface:** Interactive text menu system
- **Comprehensive Logging:** Execution timing and structured logs

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/RubyJane88/acit4420_finalassignment2025.git
cd acit4420_finalassignment2025

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Development Setup

### TDD Workflow

```bash
# Start continuous testing (recommended for TDD)
ptw

# Run specific tests
pytest tests/test_courier.py -v

# Run with coverage
pytest --cov=courier_optimizer --cov-report=html
```

### Code Quality

```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy courier_optimizer/
```

## 📁 Project Structure

```
courier_optimizer/          # Main package
├── __init__.py
├── models/                 # Data models
├── optimization/           # Route optimization algorithms
├── validation/            # Input validation
├── cli/                   # Command-line interface
└── utils/                 # Utilities and helpers

tests/                     # Test suite
data/                      # Sample data files
logs/                      # Log files
output/                    # Generated route files
.docs/                     # Local documentation (not committed)
```

## 📊 Usage

### Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the interactive CLI
python cli.py
```

### CLI Workflow

1. **Select Operation:** Choose "Optimize delivery route"
2. **Select Transport Mode:**
   - Car: Fast (50 km/h), 4 NOK/km, 120g CO2/km
   - Bicycle: Medium (15 km/h), Free, Zero emissions
   - Walking: Slow (5 km/h), Free, Zero emissions
3. **Select Optimization Criteria:**
   - FASTEST: Minimize total delivery time
   - CHEAPEST: Minimize total cost
   - GREENEST: Minimize CO2 emissions
4. **View Results:** Check output files and console summary

### Example Session

```
👋 Welcome to CourierOptimizer!

============================================================
  COURIER OPTIMIZER - Route Planning System
============================================================

What would you like to do?
  1. Optimize delivery route
  2. Exit

Enter your choice (1-2): 1

------------------------------------------------------------
  SELECT TRANSPORT MODE
------------------------------------------------------------

🚗 Available transport modes:
  1. CAR     - Fast (50 km/h), Costs 4 NOK/km, 120g CO2/km
  2. BICYCLE - Medium (15 km/h), Free, Zero emissions
  3. WALKING - Slow (5 km/h), Free, Zero emissions

Enter your choice (1-3): 1

✅ Selected transport mode: CAR

------------------------------------------------------------
  SELECT OPTIMIZATION CRITERIA
------------------------------------------------------------

🎯 What's most important for this delivery run?
  1. FASTEST  - Minimize total delivery time
  2. CHEAPEST - Minimize total cost
  3. GREENEST - Minimize CO2 emissions

Enter your choice (1-3): 1
✅ Selected criteria: FASTEST

============================================================
  PROCESSING DELIVERIES
============================================================

📁 Reading deliveries from data/deliveries.csv...
✅ Loaded 9 deliveries

🔍 Validating deliveries...
   ✅ Valid: 7
   ❌ Invalid: 2

🎯 Optimizing route...
✅ Optimized 7 deliveries

💾 Saving results...

============================================================
  🎉 ROUTE OPTIMIZATION COMPLETE!
============================================================

📦 Processed 7 deliveries
📏 Total distance: 49.24 km
⏱️  Total time: 0.98 hours (59 minutes)
💰 Total cost: 196.98 NOK
🌍 Total CO2: 5.91 kg

📂 Output files:
   • output/route.csv
   • output/rejected.csv
```

### Input Format

**CSV file:** `data/deliveries.csv`

Required headers: `customer,latitude,longitude,priority,weight_kg`

**Example:**

```csv
customer,latitude,longitude,priority,weight_kg
Kairo Juan,59.9139,10.7522,HIGH,15.5
Riley Chen,59.9200,10.7500,MEDIUM,8.0
Kaia Berg,59.9500,10.7500,LOW,5.0
```

**Validation Rules:**

- `customer`: Non-empty string with printable characters
- `latitude`: Float between 59.8 and 60.0 (Oslo bounds)
- `longitude`: Float between 10.6 and 10.9 (Oslo bounds)
- `priority`: Must be HIGH, MEDIUM, or LOW
- `weight_kg`: Non-negative number ≤ 25 kg

### Output Files

**1. `output/route.csv`** - Optimized delivery route

```csv
stop_number,customer,latitude,longitude,priority,weight_kg,distance_km,cumulative_distance_km,eta_hours,cost_nok,co2_grams
1,Riley Chen,59.9200,10.7500,HIGH,8.0,1.23,1.23,0.02,4.92,147.60
2,Kairo Juan,59.9139,10.7522,HIGH,15.5,0.72,1.95,0.01,2.88,86.40
...
```

**2. `output/rejected.csv`** - Invalid deliveries with warnings

```csv
customer,latitude,longitude,priority,weight_kg,warnings
Isaac Rey,62.0,11.5,INVALID,30.0,Coordinates outside Oslo|Invalid priority|Weight exceeds maximum
```

**3. `logs/run.log`** - Execution log with timing

```
2025-10-22 12:09:29 - CourierOptimizer - INFO - CourierOptimizer CLI Started
2025-10-22 12:09:29 - CourierOptimizer - INFO - User selected transport mode: CAR
2025-10-22 12:09:29 - CourierOptimizer - INFO - Starting process_deliveries()
2025-10-22 12:09:29 - CourierOptimizer - INFO - Completed process_deliveries() in 0.02s
...
```

### Configuration

**Depot Location:** Oslo City Hall (59.9114°N, 10.7343°E)

- All routes start and end at this fixed location
- Distance calculations use Haversine formula with Earth radius 6371 km

**Transport Parameters:**

| Mode    | Speed (km/h) | Cost (NOK/km) | CO2 (g/km) |
| ------- | ------------ | ------------- | ---------- |
| Car     | 50           | 4.0           | 120        |
| Bicycle | 15           | 0.0           | 0          |
| Walking | 5            | 0.0           | 0          |

**Priority Handling:**

- HIGH: Delivered first (priority weight = 1)
- MEDIUM: Delivered second (priority weight = 2)
- LOW: Delivered last (priority weight = 3)
- Within same priority, deliveries are sorted by distance from depot

## 🧪 Testing

This project follows Test-Driven Development principles:

- Comprehensive test suite with pytest
- Continuous testing with pytest-watch
- Code coverage reporting
- Integration and unit tests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ruby Jane Cabagnot**  
ACIT 4420 Scripting 2 - Fall 2025
Python Scripting
