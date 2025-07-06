# 🧮 Sci-Calc – Scientific Calculator

A comprehensive command-line scientific calculator **with advanced numerical-calculus utilities and full complex-number support**, written in pure Python.

---
## 🚀 How to Use (File-by-File Cheat-Sheet)

| File | Purpose | Typical Command |
|------|---------|-----------------|
| **`sci_calc.py`** | Interactive CLI calculator (real & complex arithmetic, trig, logs, special functions, *plus* a new *Numeric Calculus* menu) | `python sci_calc.py` |
| **`calculus.py`** | Importable numerical-calculus backend – string-to-function parser, differentiation, definite & contour integration, root finding | ```from calculus import make_func, differentiation, integration, find_root ``` |
| **`test_calc.py`** | Pytest test-suite covering **all** public functions in the program | `pytest -q test_calc.py` |
| **`requirements.txt`** | Minimal pip dependencies (✅ works inside *any* Python ≥ 3.8) | `pip install -r requirements.txt` |
| **`environment.yml`** | Complete Conda environment (Python 3.11 + compiled libs) | `conda env create -f environment.yml && conda activate CalC` |

---
## 🎯 Quick Start

### 1 · Clone & enter the project
```bash
git clone https://github.com/shadow30812/Sci-Calc.git
cd Sci-Calc
```

### 2 · Install the environment  
Choose **one** of the two options below.

<details>
<summary>🍰  Option A – pip-only (light-weight)</summary>

```bash
python -m venv .venv          # optional but recommended
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
</details>

<details>
<summary>🧩  Option B – Conda (reproducible C-libs)</summary>

```bash
conda env create -f environment.yml
conda activate CalC
```
</details>

### 3 · Run the Calculator
```bash
python sci_calc.py
```
Press `Ctrl+C` at any time to quit gracefully.

### 4 · Run the Test-Suite (optional)
```bash
pytest -q test_calc.py # requires pytest ≥ 8.4 (already in both env files)
```
The suite exercises every public function, including edge-case and error handling paths.

---
## 🔍 New in this Version

1. **`CalC/calculus.py`** – numerical-calculus toolkit:
   * `implicit_mul()` – make implicit products explicit ("2x" → "2*x").
   * `make_func()` – convert a string expression into a callable Python function using regular expressions and a custom parser function.
   * `differentiation` class  
     · `real_diff()` – complex-step derivative (≈ machine precision).  
     · `complex_diff()` – central-difference derivative for complex inputs.
   * `integration` class  
     · `interval_int()` – adaptive **(7) Gauss – (15) Kronrod** quadrature.  
     · `contour_int()` – contour integration along parametric curves (Trapezoidal + numerical dz/dt).
   * `find_root()` – Newton iteration with automatic derivative.
2. **Numerical Calculus Menu** in `sci_calc.py` (option 10) exposing all of the above from the CLI.
3. **`test_calc.py`** – 100 % function coverage via pytest.

---
## 🔧 Detailed Function Reference

### 1 · Expression Utilities
| Function | Description |
|----------|-------------|
| `implicit_mul(expr:str) -> str` | Inserts `*` where multiplication is implicit (e.g. `2x(1+z)` → `2*x*(1+z)`). |
| `make_func(expr, var_name='x')` | Returns a callable `f(val)` that evaluates *expr* with a custom-built parser; *val* may be real or complex. |

### 2 · Differentiation (`calculus.differentiation`)
| Method | Algorithm | Use-case |
|--------|-----------|----------|
| `real_diff(f, x0)` | Complex-step \(\frac{\Im f(x+ih)}{h}\) – 2nd-order, no cancellation | High-precision derivative of real-valued f |
| `complex_diff(f, z0)` | Central difference \(\frac{f(z+h)-f(z-h)}{2h}\) | General complex-valued functions |

### 3 · Integration (`calculus.integration`)
| Method | Purpose | Notes |
|--------|---------|-------|
| `interval_int(f, a, b)` | Definite integral on \([a,b]\) via adaptive Gauss–Kronrod (7,15) | Automatic error control (tolerance = 1e-15) |
| `contour_int(f, z(t), t₀, t₁, N)` | Contour integral \(\int_C f(z)\,dz\) with Trapezoidal rule along parametric curve | Provide `z` as callable; `N` subdivisions (default 1000) |

### 4 · Root Finding
`find_root(f, guess)` – Newton iterations using automatic `complex_diff`; stops when update < 1e-15.

---
## 🧪 Running & Understanding the Tests

* All tests reside in **`test_calculator.py`** and rely solely on **pytest**.
* Execute with `pytest -q` (quiet) or `pytest -vv` for verbose.
* Coverage:
  * **calculus** – parser, diff, quadrature, contour, root solver.
  * **sci_calc** – mode toggling, input parsing, error traps, result formatting.
* Edge-case checks: small intervals, reversed limits, divide-by-zero, invalid input strings, etc.

---
## 📦 Dependencies

| Source | Key Packages |
|--------|--------------|
| `requirements.txt` |  `pytest` (testing) |
| `environment.yml` | Same as above **plus** system libs (OpenMP, ncurses, etc.) and Python 3.11 pinned for reproducibility |

---
## 🏗️ Project Structure
```
root
├── calculus.py                 # Numerical calculus
├── sci_calc.py                 # CLI application
├── test_calc.py                # Pytest suite
├── requirements.txt            # Pip deps
├── environment.yml             # Conda env
└── README.md                   # ← you are here
```

---
## ☕ Contributing & Support
Pull requests are welcome – especially new tests, bug fixes or numerical methods which can possibly enhance the performance of existing functions.

*Report issues* via the GitHub tracker.

---
> “Mathematics is the music of reason.” – James Joseph Sylvester
