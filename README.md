# 🧮 Sci-Calc – Scientific Calculator

A comprehensive command-line scientific calculator **with advanced numerical-calculus utilities and full complex-number support**, written in pure Python.

---
## 🚀 How to Use (File-by-File Cheat-Sheet)

| File | Purpose | Typical Command |
|------|---------|-----------------|
| **`scientific_calculator.py`** | Interactive CLI calculator (real & complex arithmetic, trig, logs, special functions, *plus* a new *Numeric Calculus* menu) | `python scientific_calculator.py` |
| **`CalC/calculus.py`** | Importable numerical-calculus backend – string-to-function parser, differentiation, definite & contour integration, root finding | ```python
from CalC.calculus import make_func, differentiation, integration, find_root
``` |
| **`test_calculator.py`** | Pytest test-suite covering **all** public functions in the two modules | `pytest -q` |
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
python scientific_calculator.py
```
Press `Ctrl+C` at any time to quit gracefully.

### 4 · Run the Test-Suite (optional)
```bash
pytest -q      # requires pytest ≥ 8.4 (already in both env files)
```
The suite exercises every public function, including edge-case and error handling paths.

---
## 🔍 New in this Version

1. **`CalC/calculus.py`** – numerical-calculus toolkit:
   * `implicit_mul()` – make implicit products explicit ("2x" → "2*x").
   * `make_func()` – convert a string expression into a callable Python function using *pymep*.
   * `differentiation` class  
     · `real_diff()` – complex-step derivative (≈ machine precision).  
     · `complex_diff()` – central-difference derivative for complex inputs.
   * `integration` class  
     · `interval_int()` – adaptive **(7) Gauss – (15) Kronrod** quadrature.  
     · `contour_int()` – contour integration along parametric curves (Simpson + numerical dz/dt).
   * `find_root()` – Newton iteration with automatic derivative.
2. **Numerical Calculus Menu** in `scientific_calculator.py` (option 10) exposing all of the above from the CLI.
3. **`test_calculator.py`** – 100 % function coverage via pytest.
4. Pip/Conda environment descriptors with *pymep 1.0.7* + *pytest*.

---
## 🔧 Detailed Function Reference

### 1 · Expression Utilities
| Function | Description |
|----------|-------------|
| `implicit_mul(expr:str) -> str` | Inserts `*` where multiplication is implicit (e.g. `2x(1+z)` → `2*x*(1+z)`). |
| `make_func(expr, var_name='x')` | Returns a callable `f(val)` that evaluates *expr* with **pymep**; *val* may be real or complex. |

### 2 · Differentiation (`calculus.differentiation`)
| Method | Algorithm | Use-case |
|--------|-----------|----------|
| `real_diff(f, x0)` | Complex-step \(\frac{\Im f(x+ih)}{h}\) – 2nd-order, no cancellation | High-precision derivative of real-valued f |
| `complex_diff(f, z0)` | Central difference \(\frac{f(z+h)-f(z-h)}{2h}\) | General complex-valued functions |

### 3 · Integration (`calculus.integration`)
| Method | Purpose | Notes |
|--------|---------|-------|
| `interval_int(f, a, b)` | Definite integral on \([a,b]\) via adaptive Gauss–Kronrod (7,15) | Automatic error control (tolerance = 1e-15) |
| `contour_int(f, z(t), t₀, t₁, N)` | Contour integral \(\int_C f(z)\,dz\) with Simpson 1/3 along parametric curve | Provide `z` as callable; `N` subdivisions (default 10⁶) |

### 4 · Root Finding
`find_root(f, guess)` – Newton iterations using automatic `complex_diff`; stops when update < 1e-15.

---
## 🧪 Running & Understanding the Tests

* All tests reside in **`test_calculator.py`** and rely solely on **pytest**.
* Execute with `pytest -q` (quiet) or `pytest -vv` for verbose.
* Coverage:
  * **calculus** – parser, diff, quadrature, contour, root solver.
  * **scientific_calculator** – mode toggling, input parsing, error traps, result formatting.
* Edge-case checks: small intervals, reversed limits, divide-by-zero, invalid input strings, etc.

---
## 📦 Dependencies

| Source | Key Packages |
|--------|--------------|
| `requirements.txt` | `pymep` (analytical parser), `pytest` (testing) |
| `environment.yml` | Same as above **plus** system libs (OpenMP, ncurses, etc.) and Python 3.11 pinned for reproducibility |

`pymep` brings symbolic-style parsing to numeric code; all other runtime math uses the Python standard library.

---
## 🏗️ Project Structure
```
Sci-Calc/
├── CalC/
│   └── calculus.py          # Numerical calculus backend
├── scientific_calculator.py # CLI application
├── test_calculator.py       # Pytest suite
├── requirements.txt         # Pip deps
├── environment.yml          # Conda env
└── README.md                # ← you are here
```

---
## ☕ Contributing & Support
Pull requests are welcome – especially new tests, bug fixes or numerical methods.

*Report issues* via the GitHub tracker.

---
> “Mathematics is the music of reason.” – James Joseph Sylvester
