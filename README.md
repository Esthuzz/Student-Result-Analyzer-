# Student Result Analyzer

Simple Python tool to analyze student marks from a CSV using pandas and matplotlib.

Features:
- Calculates per-student average
- Finds the topper (highest average)
- Computes pass percentage (all subjects >= pass mark)
- Produces graphs saved to `outputs/`

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Run the analyzer on the sample data:

```bash
python analyzer.py data/students.csv --show
```

Outputs (in `outputs/`): histogram, subject averages bar chart, pass-pie.
