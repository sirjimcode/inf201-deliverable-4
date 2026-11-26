"""Pytest tests for the Fraction class (INF201, Task 2)."""

import pytest
from fraction import Fraction


# Initialiser
def test_init():
    f = Fraction(3, 4)
    assert f.numerator == 3
    assert f.denominator == 4


def test_negative_denominator_becomes_positive():
    # 1/-2 should be stored as -1/2
    f = Fraction(1, -2)
    assert f.numerator == -1
    assert f.denominator == 2


def test_zero_denominator_raises():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 0)


def test_non_integer_raises():
    # Floats are not allowed
    with pytest.raises(TypeError):
        Fraction(1.5, 2)
    with pytest.raises(TypeError):
        Fraction(1, 2.0)


# Comparisons
def test_eq():
    # 1/2 and 2/4 are equal
    assert Fraction(1, 2) == Fraction(2, 4)
    assert not Fraction(1, 2) == Fraction(1, 3)


def test_ne():
    assert Fraction(1, 2) != Fraction(1, 3)
    assert not Fraction(1, 2) != Fraction(2, 4)


def test_lt():
    assert Fraction(1, 3) < Fraction(1, 2)
    assert not Fraction(1, 2) < Fraction(1, 2)


def test_le():
    assert Fraction(1, 3) <= Fraction(1, 2)
    assert Fraction(1, 2) <= Fraction(2, 4)
    assert not Fraction(2, 3) <= Fraction(1, 2)


def test_gt():
    assert Fraction(3, 4) > Fraction(2, 3)
    assert not Fraction(1, 2) > Fraction(1, 2)


def test_ge():
    assert Fraction(3, 4) >= Fraction(2, 3)
    assert Fraction(2, 4) >= Fraction(1, 2)
    assert not Fraction(1, 3) >= Fraction(1, 2)


def test_comparison_with_negative_fractions():
    # Sign position should not matter
    assert Fraction(-1, 2) < Fraction(1, 3)
    assert Fraction(1, -2) == Fraction(-1, 2)


# Arithmetic
def test_add():
    # 1/2 + 1/3 = 5/6
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)


def test_sub():
    # 1/2 - 1/3 = 1/6
    assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)


def test_mul():
    # 2/3 * 3/4 = 1/2
    assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)


def test_truediv():
    # 1/2 / 1/4 = 2
    assert Fraction(1, 2) / Fraction(1, 4) == Fraction(2, 1)


def test_division_by_negative_fraction_keeps_denominator_positive():
    # 1/2 / -1/3 = -3/2
    result = Fraction(1, 2) / Fraction(-1, 3)
    assert result == Fraction(-3, 2)
    assert result.denominator > 0


def test_division_by_zero_fraction_raises():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0, 1)
