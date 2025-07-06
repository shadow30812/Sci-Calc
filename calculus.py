"""Module for calculus related functions"""

import math
import re
from typing import Any, Callable, Final, Self

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


def preprocess_power(expr: str) -> str:
    # Replace ^ with **, but avoid bitwise xor contexts by a simple rule:
    # Only replace ^ when between valid operand characters
    return re.sub(r"(?<=\w)\^(?=\w|\()", "**", expr)


def make_func(expr_string: str, var_name: str = "x") -> Callable[..., complex]:
    """
    Create a Python-evaluated function f(value) -> complex.
    """
    expr: str = preprocess_power(implicit_mul(expr_string))
    safe_globals: dict[Any, Any] = {}
    # Only allow math and cmath names to prevent malicious eval
    safe_locals: dict[str, complex] = {var_name: 0 + 0j}
    import cmath as _c
    import math as _m

    safe_locals.update({k: getattr(_m, k) for k in dir(_m) if not k.startswith("_")})
    safe_locals.update({k: getattr(_c, k) for k in dir(_c) if not k.startswith("_")})

    def f(value) -> complex:
        # ensure value is Python complex
        safe_locals[var_name] = value
        return complex(eval(expr, safe_globals, safe_locals))

    return f


def find_root(func: Callable[[complex], complex], guess0: float | complex) -> complex:
    guess = complex(guess0)
    iteration = 0
    while True:
        iteration += 1
        func_eval: float | complex = func(guess)
        func_eval_dash: float | complex = differentiation().complex_diff(
            func=func, point=guess
        )
        if abs(func_eval_dash) < TOL:
            # Avoid division by zero
            print("Warning: Derivative too small, stopping root finding")
            return 0 + 0j
        new_guess: complex = guess - func_eval / func_eval_dash
        if abs(new_guess - guess) < TOL:
            return new_guess
        guess: complex = new_guess
        if iteration > iter_max:
            if abs(new_guess - guess) < h:
                return new_guess


class differentiation:
    """
    Handler of real and complex numerical differentiation
    """

    def real_diff(self: Self, func: Callable[..., float], point: float) -> float:
        """
        Uses complex-step differential for excellent balance in speed and accuracy
        """
        try:
            arg = complex(point, h)
            func_result: complex = func(arg)
            if hasattr(func_result, "imag"):
                func_dash: float = complex(func_result).imag / h
            else:
                # Fallback to finite difference
                func_dash: float = (func(point + h) - func(point - h)) / (2 * h)
            return func_dash
        except Exception:
            # Fallback to finite difference
            try:
                func_dash: float = (func(point + h) - func(point - h)) / (2 * h)
                return func_dash
            except Exception:
                # Too many exceptions
                return 0.0

    def complex_diff(
        self: Self, func: Callable[[complex], complex], point: float | complex
    ) -> complex:
        """
        Uses centre finite difference for tackling every kind of complex differentiation
        without heavy computational overhead
        """
        try:
            delta_z = complex(h, h)
            high: complex = point + delta_z
            low: complex = point - delta_z
            func_dash: complex = (func(high) - func(low)) / (2 * delta_z)
            return func_dash
        except Exception:
            return 0 + 0j


class integration:
    """
    Handler of real and complex(primary) definite and interval contour integration
    """

    def interval_int(
        self: Self, func: Callable[[float], float | complex], low: float, high: float
    ) -> float | complex:
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
        GAUSS_NODES: list[float] = [
            -0.9491079123427585,
            -0.7415311855993944,
            -0.4058451513773972,
            0.0,
            0.4058451513773972,
            0.7415311855993944,
            0.9491079123427585,
        ]

        GAUSS_WEIGHTS: list[float] = [
            0.1294849661688697,
            0.2797053914892767,
            0.3818300505051189,
            0.4179591836734694,
            0.3818300505051189,
            0.2797053914892767,
            0.1294849661688697,
        ]

        # Pre-computed 15-point Kronrod nodes and weights on [-1, 1]
        KRONROD_NODES: list[float] = [
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

        KRONROD_WEIGHTS: list[float] = [
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

        def _gk_single_interval(
            func: Callable[[float], float | complex], a: float, b: float
        ) -> tuple[float | complex, float | complex]:
            """
            Compute Gauss-7 and Kronrod-15 approximations for a single interval [a, b]
            """
            # Transform nodes from [-1, 1] to [a, b]
            half_length: float = (b - a) * 0.5
            midpoint: float = (a + b) * 0.5

            # Compute Gauss-7 approximation
            gauss_sum = 0.0
            for i in range(7):
                x: float = half_length * GAUSS_NODES[i] + midpoint
                try:
                    gauss_sum += GAUSS_WEIGHTS[i] * func(x)
                except Exception:
                    # Handle function evaluation errors
                    continue
            gauss_result: float | complex = half_length * gauss_sum

            # Compute Kronrod-15 approximation
            kronrod_sum = 0.0
            for i in range(15):
                x = half_length * KRONROD_NODES[i] + midpoint
                try:
                    kronrod_sum += KRONROD_WEIGHTS[i] * func(x)
                except Exception:
                    # Handle function evaluation errors
                    continue
            kronrod_result: float | complex = half_length * kronrod_sum

            return gauss_result, kronrod_result

        def _adaptive_gk(
            func: Callable[[float], float | complex],
            a: float,
            b: float,
            depth: int,
            tol=TOL,
            max_depth=50,
        ) -> float | complex:
            """
            Recursive adaptive Gauss-Kronrod integration
            """
            if depth > max_depth:
                # Fallback to simple midpoint rule if max depth exceeded
                try:
                    return (b - a) * func((a + b) * 0.5)
                except Exception:
                    return 0.0

            try:
                touple: tuple[float | complex, float | complex] = _gk_single_interval(
                    func, a, b
                )
                gauss_result, kronrod_result = touple
            except Exception:
                # If function evaluation fails, return 0
                return 0.0

            # Error estimate
            error_estimate: float = abs(kronrod_result - gauss_result)

            # Check convergence (absolute and relative tolerance)
            tolerance: float = tol * max(1.0, abs(kronrod_result))

            if error_estimate <= tolerance or abs(b - a) < 1e-15:
                return kronrod_result

            # Subdivide and recurse
            midpoint_val: float = (a + b) * 0.5
            left_result: float | complex = _adaptive_gk(
                func, a, midpoint_val, depth + 1, tol, max_depth
            )
            right_result: float | complex = _adaptive_gk(
                func, midpoint_val, b, depth + 1, tol, max_depth
            )

            return left_result + right_result

        # Start the adaptive integration
        try:
            return _adaptive_gk(func, low, high, 0)
        except Exception as e:
            print(f"Integration failed: {e}")
            return 0.0

    def contour_int(
        self: Self,
        func: Callable[[float | complex], float | complex],
        cont: Callable[[float], float | complex],
        low: float,
        high: float,
        N: int,
    ) -> complex:
        """
        Uses numerical differentiation to convert into real integral form, then uses trapezoidal rule
        for stable and accurate integration
        """

        try:
            dt: float = (high - low) / N
            total: complex = 0.0 + 0.0j

            # Use trapezoidal rule for more stable integration
            for i in range(N + 1):
                t: float = low + i * dt

                # Calculate weight for trapezoidal rule
                if i == 0 or i == N:
                    weight = 0.5
                else:
                    weight = 1.0

                try:
                    # Evaluate contour at t
                    z_t: float | complex = cont(t)

                    # Calculate derivative numerically with central difference
                    dt_small: float = min(dt * 0.001, h * 100)
                    if i == 0:
                        # Forward difference at start
                        dz_t = (cont(t + dt_small) - cont(t)) / dt_small
                    elif i == N:
                        # Backward difference at end
                        dz_t = (cont(t) - cont(t - dt_small)) / dt_small
                    else:
                        # Central difference in middle
                        dz_t: float | complex = (
                            cont(t + dt_small) - cont(t - dt_small)
                        ) / (2 * dt_small)

                    # Add contribution to integral
                    total += weight * func(z_t) * dz_t
                except Exception:
                    # Skip problematic points
                    continue

            return total * dt

        except Exception as e:
            print(f"Contour integration failed: {e}")
            return complex(0, 0)
