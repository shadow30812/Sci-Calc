#!/usr/bin/env python3
"""
Scientific Calculator with Complex Number Support
A comprehensive command-line scientific calculator supporting:
- Basic arithmetic operations
- Advanced mathematical functions
- Trigonometric and hyperbolic functions
- Complex number operations using Euler's formulas
- Logarithmic and exponential functions
- Special mathematical functions
"""

# Uses python=3.11.13

import cmath
import math
from sys import exit, float_info
from typing import Any, Callable, Final, Literal

import calculus

# Mathematical constants
pi: Final[float] = math.pi
e: Final[float] = math.e
TOL: Final[float] = calculus.TOL
precision_epsilon: Final[float] = math.pow(
    10, -9
)  # Used for avoiding rounding errors in case of floating point numbers


class ScientificCalculator:
    """A comprehensive text-based scientific calculator with complex number support"""

    def __init__(self) -> None:
        self.complex_mode = False
        self.running = True

    def display_intro(self) -> None:
        """Display calculator introduction and basic information"""
        print("=" * 60)
        print("           SCIENTIFIC CALCULATOR")
        print("=" * 60)
        print("Welcome to the Advanced Scientific Calculator!")
        print("\nThis calculator supports:")
        print("• Basic arithmetic operations")
        print("• Advanced mathematical functions")
        print("• Trigonometric and hyperbolic functions")
        print("• Complex number operations")
        print("• Logarithmic and exponential functions")
        print("• Numerical calculus functions")
        print("\nIMPORTANT NOTES:")
        print("• All angles are in RADIANS for trigonometric functions")
        print("• Complex numbers are in the form a+ib (where i = √(-1))")
        print("• Constants 'pi' and 'e' are available for calculations")
        print("=" * 60)

    def display_menu(self) -> None:
        """Display the main menu options"""
        mode_indicator: Literal["[COMPLEX MODE]"] | Literal["[REAL MODE]"] = (
            "[COMPLEX MODE]" if self.complex_mode else "[REAL MODE]"
        )
        print(f"\n{mode_indicator} MAIN MENU:")
        print("0.  Exit the calculator")
        print("1.  Basic Arithmetic")
        print("2.  Power & Root Operations")
        print("3.  Trigonometric Functions")
        print("4.  Hyperbolic Functions")
        print("5.  Inverse Trigonometric Functions")
        print("6.  Logarithmic Functions")
        print("7.  Special Functions")
        print("8.  Toggle Complex Mode")
        print("9.  Help & Constants")
        print("10. Numerical calculus functions")
        print("-" * 40)

    def get_number_input(self, prompt="Enter number: ") -> float | complex:
        """Get number input from user, supporting both real and complex numbers"""
        while True:
            try:
                user_input: str = input(prompt).strip()

                # Handle constants
                if user_input.lower() == "pi":
                    return pi
                elif user_input.lower() == "e":
                    return e

                # Try to parse as complex number first
                if "j" in user_input or "i" in user_input:
                    # Replace 'i' with 'j' for Python complex notation
                    user_input = user_input.replace("i", "j")
                    return complex(user_input)
                else:
                    # Try to parse as float
                    num = float(user_input)
                    if abs(num) <= float_info.epsilon and num:
                        print(
                            f"Input values cannot be smaller than machine epsilon: {float_info.epsilon}"
                        )
                        print("Exiting now...")
                        exit(1)
                    return complex(num) if self.complex_mode else num

            except ValueError:
                print(
                    "Invalid input. Please enter a valid number, 'pi', 'e', or complex number (e.g., 3+4j)"
                )

    def safe_operation(self, operation, *args) -> Any:
        """Safely execute mathematical operations with error handling"""
        try:
            result: complex = operation(*args)
            return result
        except ZeroDivisionError:
            print("Error: Division by zero!")
            return None
        except ValueError as e:
            print(f"Math Error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def display_result(self, result) -> None:
        """Display calculation result in appropriate format"""
        if result is None:
            return

        if isinstance(result, complex):
            # Format complex number nicely
            real_part: float | Literal[0] = result.real if abs(result.real) > TOL else 0
            imag_part: float | Literal[0] = result.imag if abs(result.imag) > TOL else 0
            for part in [real_part, imag_part]:
                rel_error: float = part * precision_epsilon
                if part - int(part) < rel_error:
                    part = int(part)

            if imag_part == 0:
                print(f"Result: {real_part}")
            elif real_part == 0:
                print(f"Result: {imag_part}i")
            else:
                if imag_part > 0:
                    print(f"Result: {real_part} + {imag_part}i")
                else:
                    print(f"Result: {real_part} - {abs(imag_part)}i")
        else:
            if not (isinstance(result, float)):
                return
            elif result == 0:
                print("Result: 0")
            elif abs(result) < TOL:
                print(
                    f"Result ≈ 0, likely due to precision errors.\nExact Result: {result}"
                )
            else:
                rel_error = result * precision_epsilon
                if result - int(result) < rel_error:
                    result = int(result)
                print(f"Result: {result}")

    def basic_arithmetic(self) -> None:
        """Handle basic arithmetic operations"""
        print("\nBASIC ARITHMETIC OPERATIONS:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Floor Division (//)")
        print("6. Modulo (%)")
        print("7. Absolute Value (|x|)")

        choice: str = input("Select operation (1-7): ").strip()

        if choice in ["1", "2", "3", "4", "5", "6"]:
            num1: float | complex = self.get_number_input("Enter first number: ")
            num2: float | complex = self.get_number_input("Enter second number: ")

            if choice == "1":  # Addition
                result: float | complex = self.safe_operation(
                    lambda x, y: x + y, num1, num2
                )
            elif choice == "2":  # Subtraction
                result = self.safe_operation(lambda x, y: x - y, num1, num2)
            elif choice == "3":  # Multiplication
                result = self.safe_operation(lambda x, y: x * y, num1, num2)
            elif choice == "4":  # Division
                result = self.safe_operation(lambda x, y: x / y, num1, num2)
            elif choice == "5":  # Floor division
                if (
                    self.complex_mode
                    or isinstance(num1, complex)
                    or isinstance(num2, complex)
                ):
                    print("Floor division is not supported in complex mode.")
                    return
                result = self.safe_operation(lambda x, y: x // y, num1, num2)
            elif choice == "6":  # Modulo
                if (
                    self.complex_mode
                    or isinstance(num1, complex)
                    or isinstance(num2, complex)
                ):
                    print("Modulo operation is not supported in complex mode.")
                    return
                result = self.safe_operation(lambda x, y: x % y, num1, num2)
            elif choice == "7":  # Absolute value (modulus for complex numbers)
                num: float | complex = self.get_number_input("Enter number: ")
                result = self.safe_operation(
                    abs, num
                )  # This gives the modulus for complex numbers
            else:
                print("Invalid choice!")
                return

            self.display_result(result)

    def power_operations(self) -> None:
        """Handle power and root operations"""
        print("\nPOWER & ROOT OPERATIONS:")
        print("1. Exponentiation (a^x)")
        print("2. Power (x^n)")
        print("3. Square Root")
        print("4. nth Root")

        choice: str = input("Select operation (1-4): ").strip()

        if choice == "1":
            base: float | complex = self.get_number_input("Enter base (a): ")
            exponent: float | complex = self.get_number_input("Enter exponent (x): ")
            if (
                self.complex_mode
                or isinstance(base, complex)
                or isinstance(exponent, complex)
            ):
                # Using Euler's formula: a^x = exp(x * ln(a))
                result: float | complex = self.safe_operation(
                    cmath.exp, exponent * cmath.log(base)
                )
            else:
                result = self.safe_operation(pow, base, exponent)

        elif choice == "2":
            base = self.get_number_input("Enter base (x): ")
            exponent = self.get_number_input("Enter power (n): ")
            result = self.safe_operation(pow, base, exponent)

        elif choice == "3":
            num: float | complex = self.get_number_input("Enter number: ")
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.sqrt, num)
            else:
                result = self.safe_operation(math.sqrt, num)

        elif choice == "4":
            num = self.get_number_input("Enter number: ")
            root: float | complex = self.get_number_input("Enter root (n): ")
            result = self.safe_operation(pow, num, 1 / root)

        else:
            print("Invalid choice!")
            return

        self.display_result(result)

    def trigonometric_functions(self) -> None:
        """Handle trigonometric functions"""
        print("\nTRIGONOMETRIC FUNCTIONS (angles in radians):")
        print("1. sin(x)")
        print("2. cos(x)")
        print("3. tan(x)")
        print("4. sec(x)")
        print("5. csc(x)")
        print("6. cot(x)")

        choice: str = input("Select function (1-6): ").strip()
        num: float | complex = self.get_number_input("Enter angle in radians: ")

        if choice == "1":  # sin
            if self.complex_mode or isinstance(num, complex):
                result: float | complex = self.safe_operation(cmath.sin, num)
            else:
                result = self.safe_operation(math.sin, num)
        elif choice == "2":  # cos
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.cos, num)
            else:
                result = self.safe_operation(math.cos, num)
        elif choice == "3":  # tan
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.tan, num)
            else:
                result = self.safe_operation(math.tan, num)
        elif choice == "4":  # sec
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: 1 / cmath.cos(x), num)
            else:
                result = self.safe_operation(lambda x: 1 / math.cos(x), num)
        elif choice == "5":  # csc
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: 1 / cmath.sin(x), num)
            else:
                result = self.safe_operation(lambda x: 1 / math.sin(x), num)
        elif choice == "6":  # cot
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: 1 / cmath.tan(x), num)
            else:
                result = self.safe_operation(lambda x: 1 / math.tan(x), num)
        else:
            print("Invalid choice!")
            return

        self.display_result(result)

    def hyperbolic_functions(self) -> None:
        """Handle hyperbolic functions"""
        print("\nHYPERBOLIC FUNCTIONS:")
        print("1. sinh(x)")
        print("2. cosh(x)")
        print("3. tanh(x)")
        print("4. sech(x)")
        print("5. csch(x)")
        print("6. coth(x)")

        choice: str = input("Select function (1-6): ").strip()
        num: float | complex = self.get_number_input("Enter number: ")

        if choice == "1":  # sinh
            if self.complex_mode or isinstance(num, complex):
                result: float | complex = self.safe_operation(cmath.sinh, num)
            else:
                result = self.safe_operation(math.sinh, num)
        elif choice == "2":  # cosh
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.cosh, num)
            else:
                result = self.safe_operation(math.cosh, num)
        elif choice == "3":  # tanh
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.tanh, num)
            else:
                result = self.safe_operation(math.tanh, num)
        elif choice == "4":  # sech
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: 1 / cmath.cosh(x), num)
            else:
                result = self.safe_operation(lambda x: 1 / math.cosh(x), num)
        elif choice == "5":  # csch
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: 1 / cmath.sinh(x), num)
            else:
                result = self.safe_operation(lambda x: 1 / math.sinh(x), num)
        elif choice == "6":  # coth
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: 1 / cmath.tanh(x), num)
            else:
                result = self.safe_operation(lambda x: 1 / math.tanh(x), num)
        else:
            print("Invalid choice!")
            return

        self.display_result(result)

    def inverse_trigonometric_functions(self) -> None:
        """Handle inverse trigonometric functions"""
        print("\nINVERSE TRIGONOMETRIC FUNCTIONS (result in radians):")
        print("1. arcsin(x) / asin(x)")
        print("2. arccos(x) / acos(x)")
        print("3. arctan(x) / atan(x)")
        print("4. arcsec(x)")
        print("5. arccsc(x)")
        print("6. arccot(x)")

        choice: str = input("Select function (1-6): ").strip()
        num: float | complex = self.get_number_input("Enter number: ")

        if choice == "1":  # arcsin
            if self.complex_mode or isinstance(num, complex):
                result: float | complex = self.safe_operation(cmath.asin, num)
            else:
                result = self.safe_operation(math.asin, num)
        elif choice == "2":  # arccos
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.acos, num)
            else:
                result = self.safe_operation(math.acos, num)
        elif choice == "3":  # arctan
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.atan, num)
            else:
                result = self.safe_operation(math.atan, num)
        elif choice == "4":  # arcsec
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: cmath.acos(1 / x), num)
            else:
                result = self.safe_operation(lambda x: math.acos(1 / x), num)
        elif choice == "5":  # arccsc
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: cmath.asin(1 / x), num)
            else:
                result = self.safe_operation(lambda x: math.asin(1 / x), num)
        elif choice == "6":  # arccot
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(lambda x: cmath.atan(1 / x), num)
            else:
                result = self.safe_operation(lambda x: math.atan(1 / x), num)
        else:
            print("Invalid choice!")
            return

        self.display_result(result)

    def logarithmic_functions(self) -> None:
        """Handle logarithmic functions"""
        print("\nLOGARITHMIC FUNCTIONS:")
        print("1. Natural logarithm ln(x)")
        print("2. Common logarithm log10(x)")
        print("3. Logarithm with custom base")
        print("4. Exponential e^x")
        print("5. Exponential 10^x")

        choice: str = input("Select function (1-5): ").strip()

        if choice == "1":  # Natural logarithm
            num: float | complex = self.get_number_input("Enter number: ")
            if self.complex_mode or isinstance(num, complex):
                result: float | complex = self.safe_operation(cmath.log, num)
            else:
                result = self.safe_operation(math.log, num)

        elif choice == "2":  # Common logarithm
            num = self.get_number_input("Enter number: ")
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.log10, num)
            else:
                result = self.safe_operation(math.log10, num)

        elif choice == "3":  # Custom base logarithm
            num = self.get_number_input("Enter number: ")
            base: float | complex = self.get_number_input("Enter base: ")
            if (
                self.complex_mode
                or isinstance(num, complex)
                or isinstance(base, complex)
            ):
                # Using change of base formula: log_b(x) = ln(x) / ln(b)
                result = self.safe_operation(
                    lambda x, b: cmath.log(x) / cmath.log(b), num, base
                )
            else:
                result = self.safe_operation(math.log, num, base)

        elif choice == "4":  # e^x
            num = self.get_number_input("Enter exponent: ")
            if self.complex_mode or isinstance(num, complex):
                result = self.safe_operation(cmath.exp, num)
            else:
                result = self.safe_operation(math.exp, num)

        elif choice == "5":  # 10^x
            num = self.get_number_input("Enter exponent: ")
            result = self.safe_operation(pow, 10, num)

        else:
            print("Invalid choice!")
            return

        self.display_result(result)

    def special_functions(self) -> None:
        """Handle special mathematical functions"""
        print("\nSPECIAL FUNCTIONS:")
        print("1. Factorial (n!)")
        print("2. Degrees to Radians")
        print("3. Radians to Degrees")
        print("4. Complex conjugate")
        print("5. Phase angle (argument)")
        print("6. Polar form")
        print("7. Rectangular form")

        choice: str = input("Select function (1-7): ").strip()

        if choice == "1":  # Factorial
            num: float | complex = self.get_number_input("Enter non-negative integer: ")
            if isinstance(num, complex) and num.imag != 0:
                print(
                    "Factorial is not defined for complex numbers with non-zero imaginary part."
                )
                return
            if isinstance(num, complex):
                num = int(num.real)
            else:
                num = int(num)
            if num < 0:
                print("Factorial is not defined for negative numbers.")
                return
            result: Any = self.safe_operation(math.factorial, num)

        elif choice == "2":  # Degrees to Radians
            num = self.get_number_input("Enter angle in degrees: ")
            if isinstance(num, complex) and num.imag != 0:
                print(
                    "Angle conversion is not supported for complex numbers with non-zero imaginary part."
                )
                return
            if isinstance(num, complex):
                num = int(num.real)
            result = self.safe_operation(math.radians, num)

        elif choice == "3":  # Radians to Degrees
            num = self.get_number_input("Enter angle in radians: ")
            if isinstance(num, complex) and num.imag != 0:
                print(
                    "Angle conversion is not supported for complex numbers with non-zero imaginary part."
                )
                return
            if isinstance(num, complex):
                num = int(num.real)
            result = self.safe_operation(math.degrees, num)

        elif choice == "4":  # Complex conjugate
            num = self.get_number_input("Enter complex number: ")
            if not isinstance(num, complex):
                num = complex(num)
            result = num.conjugate()

        elif choice == "5":  # Phase angle
            num = self.get_number_input("Enter complex number: ")
            if not isinstance(num, complex):
                num = complex(num)
            result = self.safe_operation(cmath.phase, num)

        elif choice == "6":  # Polar form
            num = self.get_number_input("Enter complex number: ")
            if not isinstance(num, complex):
                num = complex(num)
            result = self.safe_operation(cmath.polar, num)
            if result:
                print(f"Polar form: r = {result[0]}, θ = {result[1]} radians")
                return
            else:
                result = 0

        elif choice == "7":  # Rectangular form
            r: float | complex = self.get_number_input("Enter magnitude (r): ")
            theta: float | complex = self.get_number_input(
                "Enter phase angle (θ) in radians: "
            )
            result = self.safe_operation(cmath.rect, r, theta)

        else:
            print("Invalid choice!")
            return

        self.display_result(result)

    def toggle_complex_mode(self) -> None:
        """Toggle between real and complex number modes"""
        self.complex_mode: bool = not self.complex_mode
        mode: Literal["COMPLEX"] | Literal["REAL"] = (
            "COMPLEX" if self.complex_mode else "REAL"
        )
        print(f"Switched to {mode} MODE")

    def help_and_constants(self) -> None:
        """Display help information and available constants"""
        print("\nHELP & CONSTANTS:")
        print("Available constants:")
        print(f"• pi = {pi}")
        print(f"• e = {e}")
        print("\nComplex number format:")
        print("• Use 'j' or 'i' for imaginary unit (e.g., 3+4j or 2-5i)")
        print("• Real numbers: 3.14, -5, 0")
        print("• Pure imaginary: 4j, -2i")
        print("\nModes:")
        print("• Real mode: Operations on real numbers")
        print("• Complex mode: All inputs treated as complex numbers")
        print(
            "\nNote: Some operations (floor division, modulo) are not available in complex mode"
        )
        print("\nDunder methods are implemented for complex number operations:")
        print("• __add__, __sub__, __mul__, __truediv__, __abs__")

    def numeric_calculus(self) -> None:
        """Handle numeric calculus functions and parsing"""
        print("\nNUMERIC CALCULUS FUNCTIONS:")
        print("1. Compute value of a function at a particular value")
        print("2. Numeric differentiation")
        print("3. Definite integration")
        print("4. Contour integration")
        print("5. Root of a function")

        choice: str = input("Select function (1-5): ").strip()
        print("Reserved keywords: 'pi', 'e', 'inf', 'epsilon'")
        print("Avoid using i or j as variable names (iotaBound)")

        if choice == "1":
            expr: str = input("Enter the function: ")
            var: str = input("Enter the variable in the function: ")
            f: Callable[[float | complex], complex] = calculus.make_func(expr, var)
            num: float | complex = self.get_number_input(
                "Enter the value at which you wish to calculate the function: "
            )
            result: float | complex = self.safe_operation(f, num)

        elif choice == "2":
            expr = input("Enter the function: ")
            var = input("Enter the variable in the function: ")
            f = calculus.make_func(expr, var)
            pt: float | complex = self.get_number_input(
                "Enter the point at which you wish to differentiate the function: "
            )
            diff = calculus.differentiation()
            type: Literal["complex"] | Literal["real"] = (
                "complex"
                if isinstance(pt, complex) or "i" in expr or "j" in expr
                else "real"
            )

            if type == "real":
                result = self.safe_operation(diff.real_diff, f, pt)
            else:
                result = diff.complex_diff(f, pt)

        elif choice == "3":
            expr = input("Enter the function: ")
            var = input("Enter the variable in the function: ")
            f = calculus.make_func(expr, var)
            a: float | complex = self.get_number_input(
                "Enter the lower limit of integration: "
            )
            b: float | complex = self.get_number_input(
                "Enter the upper limit of integration: "
            )
            result = self.safe_operation(calculus.integration().interval_int, f, a, b)

        elif choice == "4":
            func_expr: str = input("Enter the function to be integrated: ")
            func_var: str = input("Enter the variable in the function: ")
            f = calculus.make_func(func_expr, func_var)

            cont_expr: str = input("Enter the contour function: ")
            cont_var: str = input("Enter the variable in the function: ")
            z: Callable[[float | complex], complex] = calculus.make_func(
                cont_expr, cont_var
            )

            a = self.get_number_input("Enter the lower limit of integration: ")
            b = self.get_number_input("Enter the upper limit of integration: ")
            N = int(input("Intervals [default 1000]: ") or 1000)

            result = self.safe_operation(
                calculus.integration().contour_int, f, z, a, b, N
            )

        elif choice == "5":
            expr = input("Enter the function: ")
            var = input("Enter the variable in the function: ")
            f = calculus.make_func(expr, var)
            guess: float | complex = self.get_number_input("Enter initial guess: ")
            result = self.safe_operation(calculus.find_root, f, guess)

        else:
            print("Invalid choice!")
            return

        self.display_result(result)

    def run(self) -> None:
        """Run the main calculator loop"""
        self.display_intro()
        while self.running:
            self.display_menu()
            choice: str = input("Enter your choice (0-10): ").strip()

            if choice == "0":
                print("\nThank you for using CalC!")
                print("Goodbye!")
                self.running = False
            elif choice == "1":
                self.basic_arithmetic()
            elif choice == "2":
                self.power_operations()
            elif choice == "3":
                self.trigonometric_functions()
            elif choice == "4":
                self.hyperbolic_functions()
            elif choice == "5":
                self.inverse_trigonometric_functions()
            elif choice == "6":
                self.logarithmic_functions()
            elif choice == "7":
                self.special_functions()
            elif choice == "8":
                self.toggle_complex_mode()
            elif choice == "9":
                self.help_and_constants()
            elif choice == "10":
                self.numeric_calculus()
            else:
                print("Invalid choice. Please select a valid option (0-9).")

            if self.running:
                input("\nPress Enter to continue...")


def main() -> None:
    """Main function to run the calculator"""
    try:
        calculator = ScientificCalculator()
        calculator.run()
    except KeyboardInterrupt:
        print("\n\nCalculator interrupted by user (Keyboard Interrupt). Goodbye!")
    # except Exception as e:
    #     print(f"\nAn unexpected error occurred: {e}")
    #     print(
    #         "Please restart the calculator by pressing Ctrl+C and running the script again."
    #     )


if __name__ == "__main__":
    main()
