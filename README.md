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

### Input Format

CSV file with headers: `customer,latitude,longitude,priority,weight_kg`

### Output Files

- `route.csv` - Optimized delivery route
- `rejected.csv` - Invalid entries with warnings
- `run.log` - Execution log with timing
- `metrics.csv` - Performance metrics (optional)

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
