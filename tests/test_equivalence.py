from decimal import Decimal
import pytest

from fhirpathpy.engine.invocations.equality import (
    decimal_places,
    is_equivalent,
    normalize_string,
    round_to_decimal_places,
)


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("ab c", "ab c"),
        ("  A B C  ", "a b c"),
        ("dEf", "def"),
        ("  X y Z  ", "x y z"),
        ("", ""),
    ],
)
def normalize_string_test(s, expected):
    assert normalize_string(s) == expected


@pytest.mark.parametrize(
    ("a", "expected"),
    [
        (1.001, 3),
        (1.1, 1),
        (1.0, 0),
        (0, 0),
        (0.00000011, 8),
        (0.00000010, 7),
        (0.01, 2),
    ],
)
def decimal_places_test(a, expected):
    assert decimal_places(a) == expected


@pytest.mark.parametrize(
    ("a", "n", "expected"),
    [
        (1.001, 2, Decimal("1.00")),
        (1.1, 1, Decimal("1.1")),
        (1.012345, 3, Decimal("1.012")),
        (0.123456, 4, Decimal("0.1235")),
        (0, 2, Decimal("0")),
        (0.00012345, 4, Decimal("0.0001")),
    ],
)
def round_to_decimal_places_test(a, n, expected):
    assert round_to_decimal_places(a, n) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1.001, 1.0012, True),
        (1.1, 1.101, True),
        (1.012345, 1.012346, False),
        (0.123456000, 0.123457, False),
        (0.123457000, 0.123457, True),
        (0.00012345, 0.00012346, False),
        (1.0, 1, True),
        (0, 0.0001, True),
        (1, 0.0001, False),
        (0.123, 0.123456, True),
    ],
)
def is_equivalent_test(a, b, expected):
    assert is_equivalent(a, b) == expected
