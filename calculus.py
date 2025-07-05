"""Module for calculus related functions"""

import math
import re
from typing import Final

from pymep.complex import Complex as PComplex
from pymep.complexParser import eval as _eval

TOL: Final[float] = math.pow(
    10, -15
)  # Used for defining tolerance in approximate numerical calculus functions
h: Final[float] = math.pow(
    10, -12
)  # Used for defining limiting value for performing differentials
iter_max: Final[int] = int(
    math.pow(10, 6)
)  # Used for defining maximum number of iterations to avoid computational overhead


def implicit_mul(expr: str) -> str:
    r"""
    Convert implicit multiplication into explicit '*' operations.
    Examples:
      "30x"    → "30*x"
      "2x+3"   → "2*x+3"
      "(1+2)x" → "(1+2)*x"
      "2(1+2)" → "2*(1+2)"
    """
    # Between number or ')' and a variable or '('
    expr = re.sub(r"(?<=[0-9\)])(?=[A-Za-z\(])", "*", expr)

    # Between variable or ')' and number or '(' (e.g., "x2" → "x*2")
    expr = re.sub(r"(?<=[A-Za-z\)])(?=[0-9\(])", "*", expr)

    return expr


def make_func(expr_string, var_name="x"):
    """
    Factory function that creates f(value) → complex:
    - value may be real or complex
    - pass in a pymep Complex object for correct parsing
    """
    # Preprocess to insert explicit multiplication
    expr_string = implicit_mul(expr_string)

    def f(value):
        # If value is Python complex, convert to pymep.Complex
        if isinstance(value, complex):
            var_value = PComplex(value.real, value.imag)
        else:
            # Either real float or pymep.Complex already
            var_value = value

        # Supply the variable mapping directly
        result = _eval(expr_string, {var_name: var_value})
        return complex(result.__complex__())

    return f


def find_root(func, guess0):
    guess0 = complex(guess0)
    iteration = 0
    while True:
        iteration += 1
        func_eval = func(guess0)
        func_eval_dash = differentiation().complex_diff(func=func, point=guess0)
        new_guess = guess0 - func_eval / func_eval_dash
        if abs(new_guess - guess0) < TOL:
            return new_guess
        guess0 = new_guess
        if iteration > iter_max:
            if abs(new_guess - guess0) < h:
                return new_guess


class differentiation:
    """
    Handler of real and complex numerical differentiation
    """

    def real_diff(self, func, point):
        """
        Uses complex-step differential for excellent balance in speed and accuracy
        """
        arg = complex(point, h)
        func_dash = ((func(arg)).imag) / h
        return func_dash

    def complex_diff(self, func, point):
        """
        Uses centre finite difference for tackling every kind of problem without heavy computational overhead
        """
        delta_z = complex(h, h)
        high = point + delta_z
        low = point - delta_z
        func_dash = (func(high) - func(low)) / (2 * delta_z)
        return func_dash


class integration:
    """
    Handler of real and complex(primary) definite and interval contour integration
    """

    def interval_int(self, func, low, high):
        """
        Uses adaptive (7)Gauss-(15)Kronrod quadrature with Legendre polynomials as a great balance of accuracy and speed
        """
        # Handle edge cases
        if low == high:
            return 0.0

        # Ensure low < high
        if low > high:
            return -self.interval_int(func, high, low)

        # Pre-computed 7-point Gauss-Legendre nodes and weights on [-1, 1]
        GAUSS_NODES = [
            -0.9491079123427585,
            -0.7415311855993944,
            -0.4058451513773972,
            0.0,
            0.4058451513773972,
            0.7415311855993944,
            0.9491079123427585,
        ]

        GAUSS_WEIGHTS = [
            0.1294849661688697,
            0.2797053914892767,
            0.3818300505051189,
            0.4179591836734694,
            0.3818300505051189,
            0.2797053914892767,
            0.1294849661688697,
        ]

        # Pre-computed 15-point Kronrod nodes and weights on [-1, 1]
        KRONROD_NODES = [
            -0.9914553711208126,
            -0.9491079123427585,
            -0.8648644233597691,
            -0.7415311855993944,
            -0.5860872354676911,
            -0.4058451513773972,
            -0.2077849550078985,
            0.0,
            0.2077849550078985,
            0.4058451513773972,
            0.5860872354676911,
            0.7415311855993944,
            0.8648644233597691,
            0.9491079123427585,
            0.9914553711208126,
        ]

        KRONROD_WEIGHTS = [
            0.02293532201052922,
            0.06309209262997855,
            0.1047900103222502,
            0.1406532597155259,
            0.1690047266392679,
            0.1903505780647854,
            0.2044329400752989,
            0.2094821410847278,
            0.2044329400752989,
            0.1903505780647854,
            0.1690047266392679,
            0.1406532597155259,
            0.1047900103222502,
            0.06309209262997855,
            0.02293532201052922,
        ]

        def _gk_single_interval(a, b):
            """
            Compute Gauss-7 and Kronrod-15 approximations for a single interval [a, b]
            """
            # Transform nodes from [-1, 1] to [a, b]
            half_length = (b - a) * 0.5
            midpoint = (a + b) * 0.5

            # Compute Gauss-7 approximation
            gauss_sum = 0.0
            for i in range(7):
                x = half_length * GAUSS_NODES[i] + midpoint
                gauss_sum += GAUSS_WEIGHTS[i] * func(x)
            gauss_result = half_length * gauss_sum

            # Compute Kronrod-15 approximation
            kronrod_sum = 0.0
            for i in range(15):
                x = half_length * KRONROD_NODES[i] + midpoint
                kronrod_sum += KRONROD_WEIGHTS[i] * func(x)
            kronrod_result = half_length * kronrod_sum

            return gauss_result, kronrod_result

        def _adaptive_gk(a, b, depth, tol=TOL, max_depth=50):
            """
            Recursive adaptive Gauss-Kronrod integration
            """
            if depth > max_depth:
                # Fallback to simple midpoint rule if max depth exceeded
                return (b - a) * func((a + b) * 0.5)

            try:
                gauss_result, kronrod_result = _gk_single_interval(a, b)
            except Exception:
                # If function evaluation fails, return 0
                return 0.0

            # Error estimate
            error_estimate = abs(kronrod_result - gauss_result)

            # Check convergence (absolute and relative tolerance)
            tolerance = tol * max(1.0, abs(kronrod_result))

            if error_estimate <= tolerance or abs(b - a) < 1e-15:
                return kronrod_result

            # Subdivide and recurse
            midpoint_val = (a + b) * 0.5
            left_result = _adaptive_gk(a, midpoint_val, depth + 1, tol, max_depth)
            right_result = _adaptive_gk(midpoint_val, b, depth + 1, tol, max_depth)

            return left_result + right_result

        # Start the adaptive integration
        return _adaptive_gk(low, high, 0)

    def contour_int(self, func, cont, low, high, N):
        """
        Uses differential techniques to convert into interval_int type of form, then uses Simpson's 1/3rd integral
        rule with weights decided in accordance with Gauss-Legendre quadrature to integrate
        """

        dt = (high - low) / N
        sum = 0 + 0j
        for i in range(N + 1):
            t = low + i * dt
            if i in [0, N]:
                weight = 1
            elif i % 2:
                weight = 4
            else:
                weight = 2
            z_t = cont(t)
            dz_t = differentiation().complex_diff(cont, t)
            sum += weight * func(z_t) * dz_t

        return sum * dt
