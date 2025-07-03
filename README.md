# 🧮 Sci-Calc - Scientific Calculator

A comprehensive command-line scientific calculator with advanced mathematical functions and complex number support, built in Python.

## 🚀 Quick Start

### How to Use

1. **Download the repository**
   ```bash
   git clone https://github.com/shadow30812/Sci-Calc.git
   cd Sci-Calc
   ```

2. **Run the calculator**
   ```bash
   python scientific_calculator.py
   ```
   or
   ```bash
   python3 scientific_calculator.py
   ```

3. **Requirements**
   - Python 3.x
   - No external dependencies required (uses only built-in `math` and `cmath` modules)

## ✨ Features

- 🔢 **Dual Mode Operation**: Real and Complex number modes
- 📐 **Advanced Mathematical Functions**: Trigonometric, hyperbolic, and inverse functions
- 🔧 **Error Handling**: Robust error handling for mathematical operations
- 🎯 **User-Friendly Interface**: Interactive menu-driven CLI
- 📊 **Mathematical Constants**: Built-in π (pi) and e constants
- 🌟 **Complex Number Support**: Full support for complex arithmetic using Euler's formulas

## 🏗️ Architecture

The calculator is built around a single `ScientificCalculator` class that provides:
- Menu-driven interface
- Safe mathematical operations with error handling
- Mode switching between real and complex number operations
- Formatted result display

## 🔧 Mathematical Functions

### 1. Basic Arithmetic 🧮

| Function | Symbol | Description | Example |
|----------|--------|-------------|---------|
| Addition | + | Add two numbers | 5 + 3 = 8 |
| Subtraction | - | Subtract second from first | 5 - 3 = 2 |
| Multiplication | * | Multiply two numbers | 5 * 3 = 15 |
| Division | / | Divide first by second | 15 / 3 = 5 |
| Floor Division | // | Integer division (real mode only) | 15 // 4 = 3 |
| Modulo | % | Remainder after division (real mode only) | 15 % 4 = 3 |
| Absolute Value | \|x\| | Absolute value or modulus | \|−5\| = 5 |

### 2. Power & Root Operations ⚡

| Function | Formula | Description | Notes |
|----------|---------|-------------|-------|
| Exponentiation | a^x | Raise a to power x | Uses Euler's formula for complex |
| Power | x^n | Raise x to power n | Standard power operation |
| Square Root | √x | Square root of x | Complex square root supported |
| nth Root | ⁿ√x | nth root of x | Calculated as x^(1/n) |

### 3. Trigonometric Functions 📐

All trigonometric functions work with **radians** as input.

| Function | Symbol | Description | Domain |
|----------|--------|-------------|---------|
| Sine | sin(x) | Sine of x | All real/complex |
| Cosine | cos(x) | Cosine of x | All real/complex |
| Tangent | tan(x) | Tangent of x | x ≠ π/2 + nπ |
| Secant | sec(x) | 1/cos(x) | x ≠ π/2 + nπ |
| Cosecant | csc(x) | 1/sin(x) | x ≠ nπ |
| Cotangent | cot(x) | 1/tan(x) | x ≠ nπ |

### 4. Hyperbolic Functions 🌊

| Function | Symbol | Description | Formula |
|----------|--------|-------------|---------|
| Hyperbolic Sine | sinh(x) | Hyperbolic sine | (e^x - e^(-x))/2 |
| Hyperbolic Cosine | cosh(x) | Hyperbolic cosine | (e^x + e^(-x))/2 |
| Hyperbolic Tangent | tanh(x) | Hyperbolic tangent | sinh(x)/cosh(x) |
| Hyperbolic Secant | sech(x) | 1/cosh(x) | 2/(e^x + e^(-x)) |
| Hyperbolic Cosecant | csch(x) | 1/sinh(x) | 2/(e^x - e^(-x)) |
| Hyperbolic Cotangent | coth(x) | 1/tanh(x) | cosh(x)/sinh(x) |

### 5. Inverse Trigonometric Functions 🔄

Results are returned in **radians**.

| Function | Symbol | Description | Range |
|----------|--------|-------------|-------|
| Arcsine | arcsin(x) | Inverse sine | [-π/2, π/2] |
| Arccosine | arccos(x) | Inverse cosine | [0, π] |
| Arctangent | arctan(x) | Inverse tangent | (-π/2, π/2) |
| Arcsecant | arcsec(x) | Inverse secant | [0, π] |
| Arccosecant | arccsc(x) | Inverse cosecant | [-π/2, π/2] |
| Arccotangent | arccot(x) | Inverse cotangent | (0, π) |

### 6. Logarithmic Functions 📈

| Function | Symbol | Description | Base |
|----------|--------|-------------|------|
| Natural Logarithm | ln(x) | Logarithm base e | e ≈ 2.718 |
| Common Logarithm | log₁₀(x) | Logarithm base 10 | 10 |
| Custom Base Logarithm | log_b(x) | Logarithm base b | User-defined |
| Exponential e | e^x | e raised to power x | Natural exponential |
| Exponential 10 | 10^x | 10 raised to power x | Common exponential |

### 7. Special Functions 🌟

| Function | Symbol | Description | Requirements |
|----------|--------|-------------|--------------|
| Factorial | n! | Product of positive integers ≤ n | n ≥ 0, integer |
| Degrees to Radians | deg→rad | Convert degrees to radians | Real numbers only |
| Radians to Degrees | rad→deg | Convert radians to degrees | Real numbers only |
| Complex Conjugate | z* | Conjugate of complex number | Complex numbers |
| Phase Angle | arg(z) | Argument of complex number | Complex numbers |
| Polar Form | r∠θ | Magnitude and phase | Complex numbers |
| Rectangular Form | a+bi | Real and imaginary parts | From polar coordinates |

## 🔢 Complex Number Support

The calculator supports two modes:

### Real Mode
- Operations performed on real numbers
- Standard mathematical functions
- Floor division and modulo operations available

### Complex Mode
- All inputs treated as complex numbers
- Uses `cmath` module for complex operations
- Supports Euler's formulas for exponentials and logarithms

### Complex Number Input Formats
- **Standard notation**: `3+4j` or `3+4i`
- **Pure imaginary**: `4j` or `4i`
- **Real numbers**: `3.14` (automatically converted in complex mode)

## 🎯 Constants

| Constant | Symbol | Value | Usage |
|----------|--------|-------|-------|
| Pi | π | 3.14159... | Type "pi" as input |
| Euler's Number | e | 2.71828... | Type "e" as input |

## ⚠️ Important Notes

1. **Angle Units**: All trigonometric functions use **radians**
2. **Complex Numbers**: Use `j` or `i` for imaginary unit (e.g., `3+4j`)
3. **Error Handling**: Division by zero and invalid operations are handled gracefully
4. **Precision**: Results near zero may show precision warnings
5. **Mode Restrictions**: Some operations (floor division, modulo) not available in complex mode

## 🛠️ Error Handling

The calculator includes comprehensive error handling for:
- **Division by zero**: Prevents crashes and shows error message
- **Invalid mathematical operations**: Domain errors for functions like log(-1)
- **Type errors**: Graceful handling of invalid inputs
- **Overflow/underflow**: Protection against extreme values

## 🎮 Usage Examples

```bash
# Basic arithmetic
5 + 3 = 8
10 / 2 = 5.0

# Trigonometric functions (radians)
sin(π/2) = 1.0
cos(0) = 1.0

# Complex numbers
(3+4j) + (1+2j) = 4+6j
|(3+4j)| = 5.0

# Logarithms
ln(e) = 1.0
log₁₀(100) = 2.0

# Special functions
5! = 120
```

## 📱 Interface Navigation

The calculator provides a menu-driven interface with:
- **Main Menu**: Choose operation categories (1-9)
- **Operation Menus**: Select specific functions within each category
- **Mode Toggle**: Switch between real and complex modes
- **Help System**: Built-in help and constants reference
- **Exit**: Clean exit with goodbye message

## 🔄 Development

### File Structure
```
Sci-Calc/
├── scientific_calculator.py    # Main calculator implementation
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

### Key Components
- **ScientificCalculator class**: Main calculator logic
- **Menu system**: Interactive user interface
- **Error handling**: Safe mathematical operations
- **Mode management**: Real vs complex number modes

## 📄 License

This project is available under the MIT License. Feel free to use, modify, and distribute according to the license terms.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

*"Mathematics is the language with which God has written the universe." - Galileo Galilei*