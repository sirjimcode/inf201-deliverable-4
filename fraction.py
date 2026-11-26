"""Fraction class (INF201, Task 2)."""


class Fraction:
    """Fraction with integer parts and a positive denominator."""

    def __init__(self, numerator, denominator):
        # Both parts must be integers
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("numerator and denominator must be integers")
        if denominator == 0:
            raise ZeroDivisionError("denominator cannot be zero")
        # Move the sign to the numerator: 1/-2 -> -1/2
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        self.numerator = numerator
        self.denominator = denominator

    # Comparisons
    # Cross-multiply: a/b vs c/d  ->  a*d vs c*b
    def __eq__(self, other):  # ==
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __ne__(self, other):  # !=
        return self.numerator * other.denominator != other.numerator * self.denominator

    def __lt__(self, other):  # <
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):  # <=
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):  # >
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other):  # >=
        return self.numerator * other.denominator >= other.numerator * self.denominator

    # Arithmetic
    def __add__(self, other):
        # a/b + c/d = (a*d + c*b) / (b*d)
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __sub__(self, other):
        # a/b - c/d = (a*d - c*b) / (b*d)
        return Fraction(self.numerator * other.denominator - other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __mul__(self, other):
        # a/b * c/d = (a*c) / (b*d)
        return Fraction(self.numerator * other.numerator,
                        self.denominator * other.denominator)

    def __truediv__(self, other):
        # a/b / c/d = (a*d) / (b*c)
        return Fraction(self.numerator * other.denominator,
                        self.denominator * other.numerator)
