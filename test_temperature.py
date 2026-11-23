"""Pytest tests for the Temperature class (INF201, Task 1)."""

import pytest
from temperature import Temperature


# 1. Initialisation
def test_default_unit_is_celsius():
    t = Temperature(25)
    assert t.unit == "C"
    assert t.value == 25.0


@pytest.mark.parametrize("unit, expected", [("c", "C"), ("f", "F"), ("k", "K"),
                                            ("C", "C"), ("F", "F"), ("K", "K")])
def test_unit_is_case_insensitive(unit, expected):
    assert Temperature(300, unit).unit == expected


def test_value_is_read_only():
    t = Temperature(10, "C")
    with pytest.raises(AttributeError):
        t.value = 20


def test_unit_is_read_only():
    t = Temperature(10, "C")
    with pytest.raises(AttributeError):
        t.unit = "K"


# 2. Validation
@pytest.mark.parametrize("bad_unit", ["X", "celsius", "", "R", None, 5])
def test_invalid_unit_raises(bad_unit):
    with pytest.raises(ValueError):
        Temperature(0, bad_unit)


@pytest.mark.parametrize("value, unit", [(-273.16, "C"), (-459.68, "F"), (-0.01, "K"),
                                         (-1000, "C"), (-500, "F"), (-1, "K")])
def test_below_absolute_zero_raises(value, unit):
    with pytest.raises(ValueError):
        Temperature(value, unit)


@pytest.mark.parametrize("value, unit", [(-273.15, "C"), (-459.67, "F"), (0, "K")])
def test_exactly_absolute_zero_is_allowed(value, unit):
    Temperature(value, unit)  # should not raise


@pytest.mark.parametrize("bad_target", ["X", "kelvin", ""])
def test_convert_to_invalid_unit_raises(bad_target):
    with pytest.raises(ValueError):
        Temperature(0, "C").convert_to(bad_target)


# 3. Conversions at reference points
REFERENCE_POINTS = [
    # (celsius, fahrenheit, kelvin)
    (-273.15, -459.67, 0.0),     # absolute zero
    (-40.0, -40.0, 233.15),      # C/F crossover
    (0.0, 32.0, 273.15),         # freezing point of water
    (37.0, 98.6, 310.15),        # human body temperature
    (100.0, 212.0, 373.15),      # boiling point of water
]


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_celsius(c, f, k):
    t = Temperature(c, "C")
    assert t.to_celsius() == pytest.approx(c, abs=1e-9)
    assert t.to_fahrenheit() == pytest.approx(f, abs=1e-9)
    assert t.to_kelvin() == pytest.approx(k, abs=1e-9)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_fahrenheit(c, f, k):
    t = Temperature(f, "F")
    assert t.to_celsius() == pytest.approx(c, abs=1e-9)
    assert t.to_fahrenheit() == pytest.approx(f, abs=1e-9)
    assert t.to_kelvin() == pytest.approx(k, abs=1e-9)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_kelvin(c, f, k):
    t = Temperature(k, "K")
    assert t.to_celsius() == pytest.approx(c, abs=1e-9)
    assert t.to_fahrenheit() == pytest.approx(f, abs=1e-9)
    assert t.to_kelvin() == pytest.approx(k, abs=1e-9)


@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_convert_to_returns_new_temperature(c, f, k):
    t = Temperature(c, "C")
    tf = t.convert_to("f")
    tk = t.convert_to("K")
    assert isinstance(tf, Temperature) and tf.unit == "F"
    assert isinstance(tk, Temperature) and tk.unit == "K"
    assert tf.value == pytest.approx(f, abs=1e-9)
    assert tk.value == pytest.approx(k, abs=1e-9)
    assert t.unit == "C"  # original unchanged


# 4. Round-trip conversions
@pytest.mark.parametrize("c", [-273.15, -40.0, 0.0, 25.0, 37.0, 100.0, 1234.5678])
def test_round_trip_c_f_k_c(c):
    original = Temperature(c, "C")
    result = original.convert_to("F").convert_to("K").convert_to("C")
    assert result.unit == "C"
    assert result == original
    assert result.value == pytest.approx(c, abs=1e-9)


# 5. Cross-unit comparisons
@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_equality_across_units(c, f, k):
    tc, tf, tk = Temperature(c, "C"), Temperature(f, "F"), Temperature(k, "K")
    assert tc == tf and tf == tk and tc == tk
    assert not (tc != tf)
    assert tc <= tf and tc >= tk
    assert not (tc < tf) and not (tc > tk)


def test_inequality_across_units():
    assert Temperature(0, "C") != Temperature(0, "F")
    assert Temperature(0, "K") != Temperature(0, "C")


def test_ordering_across_units():
    cold = Temperature(0, "C")         # 273.15 K
    warm = Temperature(98.6, "F")      # 310.15 K
    hot = Temperature(373.15, "K")     # 100 C
    assert cold < warm < hot
    assert hot > warm > cold
    assert cold <= warm <= hot
    assert hot >= warm >= cold
    assert not (hot < cold)
    assert not (cold >= warm)


def test_equality_within_tolerance():
    assert Temperature(0, "C") == Temperature(0 + 1e-10, "C")
    assert Temperature(0, "C") != Temperature(0 + 1e-6, "C")


def test_comparison_with_non_temperature_returns_notimplemented():
    t = Temperature(0, "C")
    for method in ("__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__"):
        assert getattr(t, method)(0) is NotImplemented
    assert (t == 0) is False
    assert (t != "0 C") is True
    with pytest.raises(TypeError):
        t < 5


def test_sorting_mixed_units():
    temps = [Temperature(212, "F"), Temperature(0, "K"), Temperature(20, "C")]
    assert [t.unit for t in sorted(temps)] == ["K", "C", "F"]


# 6. Formatting
@pytest.mark.parametrize("t, expected", [
    (Temperature(25, "C"), "25.00 °C"),
    (Temperature(98.6, "F"), "98.60 °F"),
    (Temperature(273.15, "K"), "273.15 K"),
    (Temperature(-40, "c"), "-40.00 °C"),
    (Temperature(1 / 3, "C"), "0.33 °C"),
])
def test_str(t, expected):
    assert str(t) == expected


@pytest.mark.parametrize("t, expected", [
    (Temperature(25, "C"), "Temperature(25.0, 'C')"),
    (Temperature(98.6, "f"), "Temperature(98.6, 'F')"),
    (Temperature(0, "K"), "Temperature(0.0, 'K')"),
])
def test_repr(t, expected):
    assert repr(t) == expected


def test_repr_round_trips_with_eval():
    t = Temperature(36.6, "C")
    assert eval(repr(t)) == t
