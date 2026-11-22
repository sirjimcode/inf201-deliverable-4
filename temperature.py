"""Temperature class supporting Celsius, Fahrenheit and Kelvin (INF201, Task 1)."""

from __future__ import annotations  # allows "-> Temperature" inside the class

import math

_VALID_UNITS = ("C", "F", "K")  # allowed units
_TOLERANCE = 1e-9               # tolerance for comparing floats


def _normalise_unit(unit: str) -> str:
    """Return the unit in upper case, or raise ValueError if it is invalid."""
    if not isinstance(unit, str) or unit.upper() not in _VALID_UNITS:
        raise ValueError(
            f"Invalid unit {unit!r}. Expected one of {', '.join(_VALID_UNITS)}."
        )
    return unit.upper()


class Temperature:
    """A temperature with a value and a unit ("C", "F" or "K")."""

    # __slots__ restricts the object to these two attributes only
    __slots__ = ("_value", "_unit")

    def __init__(self, value: float, unit: str = "C") -> None:
        unit = _normalise_unit(unit)   # validate and normalise the unit ("c" -> "C")
        value = float(value)           # convert to float, e.g. 25 -> 25.0
        self._value = value            # underscore = "private", not meant to be changed
        self._unit = unit
        # Check that the temperature is not below absolute zero (0 K).
        # We use a tolerance because e.g. -459.67 °F may become -0.0000000001 K
        # due to floating-point rounding errors.
        if self.to_kelvin() < -_TOLERANCE:
            raise ValueError(
                f"Temperature {value} {unit} is below absolute zero (0 K)."
            )

    # @property lets us write t.value (without parentheses), but since there
    # is no setter, t.value = 5 raises an AttributeError.
    @property
    def value(self) -> float:
        return self._value

    @property
    def unit(self) -> str:
        return self._unit

    # ----- conversions -----
    def to_celsius(self) -> float:
        if self._unit == "C":
            return self._value
        if self._unit == "K":
            return self._value - 273.15
        return (self._value - 32) * 5 / 9  # from Fahrenheit

    def to_fahrenheit(self) -> float:
        if self._unit == "F":
            return self._value
        if self._unit == "C":
            return self._value * 9 / 5 + 32
        return (self._value - 273.15) * 9 / 5 + 32  # from Kelvin

    def to_kelvin(self) -> float:
        if self._unit == "K":
            return self._value
        if self._unit == "C":
            return self._value + 273.15
        return (self._value - 32) * 5 / 9 + 273.15  # from Fahrenheit

    def convert_to(self, target_unit: str) -> Temperature:
        """Return a NEW Temperature object in the target unit."""
        target_unit = _normalise_unit(target_unit)
        # Dictionary mapping each unit to the matching conversion method
        converters = {
            "C": self.to_celsius,
            "F": self.to_fahrenheit,
            "K": self.to_kelvin,
        }
        new_value = converters[target_unit]()
        # Rounding errors can give e.g. -1e-14 K; set it to 0 instead
        if target_unit == "K" and -_TOLERANCE < new_value < 0:
            new_value = 0.0
        return Temperature(new_value, target_unit)

    # ----- string representations -----
    def __repr__(self) -> str:
        # Unambiguous version for developers, e.g. Temperature(25.0, 'C')
        return f"Temperature({self._value!r}, {self._unit!r})"

    def __str__(self) -> str:
        # Human-readable version with two decimals, e.g. "25.00 °C" or "273.15 K"
        symbol = "K" if self._unit == "K" else f"°{self._unit}"
        return f"{self._value:.2f} {symbol}"

    # ----- comparisons (all done in Kelvin) -----
    def _is_close(self, other: Temperature) -> bool:
        """True if the temperatures are equal within the 1e-9 tolerance."""
        return math.isclose(
            self.to_kelvin(), other.to_kelvin(), rel_tol=0.0, abs_tol=_TOLERANCE
        )

    # All comparisons return NotImplemented if the other object is not a
    # Temperature. Python then tries other options, and in the end
    # == gives False, while < raises a TypeError.
    def __eq__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._is_close(other)

    def __ne__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self._is_close(other)

    def __lt__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() and not self._is_close(other)

    def __le__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() or self._is_close(other)

    def __gt__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() and not self._is_close(other)

    def __ge__(self, other: object):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() or self._is_close(other)

    # Equal objects must have equal hashes. Since "equal" here means
    # "almost equal" (tolerance), that is impossible, so the class is unhashable.
    __hash__ = None
