## 🎯 OVERVIEW

**Development Approach:** Test-Driven Development (TDD)

## 📦 Projects

### Part I: CourierOptimizer ✅

**Status:** Complete

Smart courier routing system for Oslo's delivery service NordicExpress. Optimizes delivery routes based on time, cost, or environmental impact.

**Key Features:**

- Route optimization (fastest/cheapest/greenest)
- Multiple transport modes (car, bicycle, walking)
- CSV input validation with regex
- Interactive CLI with text menu
- Comprehensive logging with execution timing

**[📖 View Full Documentation →](courier_optimizer/README.md)**

**Quick Start:**

```bash
source .venv/bin/activate
python cli.py
```

---

### Part II: Conway's Game of Life ✅

**Status:** Complete with hybrid implementation

Cellular automaton simulator implementing Conway's Game of Life with both ASCII and interactive pygame visualization.

**Key Features:**

- Complete Conway's Game of Life engine with mathematical accuracy
- 7 famous patterns (Blinker, Glider, Block, Beehive, Toad, Beacon, Loaf)
- Dual visualization: ASCII CLI + Interactive pygame graphics
- Pattern library with historical significance and metadata
- Real-time animation with user controls
- Mouse interaction and keyboard shortcuts
- Comprehensive test coverage (38 tests passing)

**Demo Options:**

```bash
# ASCII CLI version
python conways_cli.py

# Interactive pygame demo
python demo_pygame_integration.py

# Focused blinker demo
python blinker_demo.py

# Animated pattern showcase
python animated_demo.py
```

**[📖 View Full Documentation →](game_of_life/README.md)**

---


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

## � Repository Structure

```
acit4420_finalassignment2025/
│
├── courier_optimizer/      # Part I: CourierOptimizer
│   ├── README.md           # Detailed documentation
│   ├── courier_optimizer.py
│   └── logger.py
│
├── game_of_life/          # Part II: Conway's Game of Life (coming soon)
│   └── README.md
│
├── tests/                 # Test suite
├── data/                  # Input data files
├── output/                # Generated output files
├── logs/                  # Application logs
├── .docs/                 # Development notes (local only)
│
├── cli.py                 # Part I CLI entry point
├── demo.py                # Part I demo script
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🔧 Development

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=courier_optimizer --cov-report=html

# Continuous testing (TDD mode)
ptw
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

## 📊 Progress Tracking

| Part | Project               | Status      | Coverage | Documentation |
| ---- | --------------------- | ----------- | -------- | ------------- |
| I    | CourierOptimizer      | ✅ Complete | 94%      | ✅ Complete   |
| II   | Conway's Game of Life | ✅ Complete | 100%     | ✅ Complete   |
| III  | [Not Required]        | -           | -        | -             |

**Combined Statistics:**

- **Total Tests:** 51 tests passing (13 CourierOptimizer + 38 Conway's Game of Life)
- **Overall Coverage:** Excellent across both projects
- **Code Quality:** No linting errors, comprehensive type hints
- **Documentation:** Professional-grade with development notes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**582**

---

_For detailed documentation on each project, please refer to the individual README files in their respective directories._
