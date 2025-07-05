# test_calculator.py
"""Pytest unit tests for calculus.py and scientific_calculator.py.

These tests use monkeypatch and capsys to simulate user interaction where needed.
All public functions and methods are covered with representative normal cases,
edge cases and common failure paths.

Run with:
    pytest -q test_calculator.py
"""

import builtins
import math

import pytest
import scientific_calculator as sc

# Import target modules
import CalC.calculus as calculus

###########################
# Tests for calculus.py   #
###########################


def test_implicit_mul_basic():
    assert calculus.implicit_mul("2x+3") == "2*x+3"
    assert calculus.implicit_mul("(1+2)x") == "(1+2)*x"
    assert calculus.implicit_mul("2(1+2)") == "2*(1+2)"
    assert calculus.implicit_mul("5sin(x)") == "5*sin(x)"  # generic alpha chars


def test_make_func_and_eval():
    f = calculus.make_func("x**2 + 2*x + 1")
    assert pytest.approx(f(2.0)) == 9.0  # (2+1)^2


def test_real_diff_accuracy():
    # derivative of sin(x) at x=0 should be cos(0)=1
    f = math.sin
    d = calculus.differentiation()
    assert pytest.approx(d.real_diff(f, 0.0), rel=1e-9) == 1.0


def test_complex_diff_accuracy():
    # derivative of f(z)=z^2 at z=1+1j is 2z = 2+2j
    def f(z):
        return z**2

    z0 = 1 + 1j
    d = calculus.differentiation()
    approx = d.complex_diff(f, z0)
    assert pytest.approx(approx.real, rel=1e-6) == 2 * z0.real
    assert pytest.approx(approx.imag, rel=1e-6) == 2 * z0.imag


def test_interval_int_simple():
    integ = calculus.integration()

    def f(x):
        return x  # integral from 0 to 1 is 0.5

    result = integ.interval_int(f, 0.0, 1.0)
    assert pytest.approx(result, rel=1e-10) == 0.5


def test_interval_int_reversed_limits():
    integ = calculus.integration()

    def f(x):
        return x**2  # integral 0..1 is 1/3, reversed should be -1/3

    result = integ.interval_int(f, 1.0, 0.0)
    assert pytest.approx(result, rel=1e-10) == -1.0 / 3.0


def test_find_root_quadratic():
    def f(x):
        return x**2 - 4

    root = calculus.find_root(f, guess0=3)
    assert pytest.approx(root, rel=1e-9) == 2.0


###############################
# Tests for ScientificCalculator
###############################


# Helper to create calculator instance without running interactive loop
@pytest.fixture()
def calc():
    return sc.ScientificCalculator()


def test_toggle_complex_mode(calc):
    initial = calc.complex_mode
    calc.toggle_complex_mode()
    assert calc.complex_mode is (not initial)


def test_safe_operation_zero_division(calc):
    res = calc.safe_operation(lambda x, y: x / y, 1, 0)
    assert res is None  # Should capture division by zero and return None


def test_get_number_input_numeric(monkeypatch, calc):
    monkeypatch.setattr(builtins, "input", lambda _: "3.5")
    assert calc.get_number_input() == 3.5


def test_get_number_input_pi(monkeypatch, calc):
    monkeypatch.setattr(builtins, "input", lambda _: "pi")
    assert calc.get_number_input() == math.pi


def test_get_number_input_complex(monkeypatch, calc):
    monkeypatch.setattr(builtins, "input", lambda _: "2+3i")
    assert calc.get_number_input() == complex(2, 3)


def test_display_result_real(capsys, calc):
    calc.display_result(0.123456)
    captured = capsys.readouterr()
    assert "0.123456" in captured.out


def test_display_result_complex(capsys, calc):
    calc.display_result(3 + 4j)
    captured = capsys.readouterr()
    assert "3" in captured.out and "4i" in captured.out


#################################
# Edge-case tests for calculus   #
#################################


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("", ""),
        ("42", "42"),
        ("(x+1)(x-1)", "(x+1)*(x-1)"),
    ],
)
def test_implicit_mul_edge(expr, expected):
    assert calculus.implicit_mul(expr) == expected


def test_interval_int_small_interval():
    integ = calculus.integration()
    f = math.sin
    a, b = 0.0, 1e-9
    res = integ.interval_int(f, a, b)
    # Approximate sin(x) ~ x in small interval, integral ~ (b^2)/2
    assert pytest.approx(res, rel=1e-6) == (b**2) / 2
