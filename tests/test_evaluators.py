import datetime
import math
import pytest
from freezegun import freeze_time

from fhirpathpy import evaluate
from fhirpathpy.engine.invocations.constants import constants

from fhirpathpy import dsl


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"a": 42}, "a + 2", [44]),
        ({"a": 42}, "a - 2", [40]),
        ({"a": 42}, "a * 2", [84]),
        ({"a": 42}, "a / 2", [21.0]),
        ({"a": 42}, "a mod 2", [0]),
        ({"a": 42}, "a div 2", [21]),
    ],
)
def infix_math_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        # or
        ({"a": True, "b": True}, "a or b", [True]),
        ({"a": True, "b": False}, "a or b", [True]),
        ({"a": False, "b": False}, "a or b", [False]),
        # and
        ({"a": True, "b": True}, "a and b", [True]),
        ({"a": True, "b": False}, "a and b", [False]),
        ({"a": False, "b": False}, "a and b", [False]),
        # xor
        ({"a": True, "b": True}, "a xor b", [False]),
        ({"a": True, "b": False}, "a xor b", [True]),
        ({"a": False, "b": False}, "a xor b", [False]),
        # implies
        ({"a": True, "b": True}, "a implies b", [True]),
        ({"a": True, "b": False}, "a implies b", [False]),
        ({"a": False, "b": False}, "a implies b", [True]),
    ],
)
def simple_logic_expressions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"a": -42}, "a.abs()", [42]),
        ({"a": 42.25}, "a.ceiling()", [43]),
        ({"a": 42.75}, "a.ceiling()", [43]),
        ({"a": 42.25}, "a.floor()", [42]),
        ({"a": 42.75}, "a.floor()", [42]),
        ({"a": 42.25}, "a.round(-1)", [40]),
        ({"a": 42.25}, "a.round(0)", [42]),
        ({"a": 42.25}, "a.round(1)", [42.2]),
        ({"a": 9}, "a.sqrt()", [3]),
        ({"a": 3}, "a.exp()", [math.exp(3)]),
        ({"a": 3}, "a.ln()", [math.log(3)]),
        ({"a": 3}, "a.log(3)", [math.log(3, 3)]),
        ({"a": 3}, "a.truncate()", [math.trunc(3)]),
    ],
)
def math_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"a": "lorem ipsum"}, "a.indexOf('ipsum')", [6]),
        ({"a": "lorem ipsum"}, "a.substring(6, 2)", ["ip"]),
        ({"a": "lorem ipsum"}, "a.startsWith('lorem')", [True]),
        ({"a": "lorem ipsum"}, "a.endsWith('ipsum')", [True]),
        ({"a": "lorem ipsum"}, "a.contains('sum')", [True]),
        ({"a": "lorem ipsum"}, "a.replace('rem', 'l')", ["lol ipsum"]),
        ({"a": "lorem ipsum"}, "a.matches('l.+')", [True]),
        ({"a": "lorem ipsum"}, "a.matches('k.+')", [False]),
        ({"a": "lorem ipsum"}, "a.replaceMatches('lorem|ipsum', 'go')", ["go go"]),
        ({"a": "lorem ipsum"}, "a.length()", [11]),
    ],
)
def string_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


"""
'select'
'ofType'
"""


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"list": []}, "list.single()", []),
        ({"list": [1]}, "list.single()", [1]),
        ({"list": [2, 3]}, "list.first()", [2]),
        ({"list": [2, 3]}, "list.last()", [3]),
        # ({"list": [{"list": {"attr":1}}]}, "list.repeat(attr)", [1]),
        # ({"list": [{"attr": True}, {"attr": True}]}, "list.repeat(attr)", [3]),
        ({"list": [1, 2, 3, 4]}, "list.tail()", [2, 3, 4]),
        ({"list": [1, 2, 3, 4]}, "list.take(2)", [1, 2]),
        ({"list": [1, 2, 3, 4]}, "list.skip(2)", [3, 4]),
        ({"list": [1, 2, 3, 4]}, "list.where($this <= 2)", [1, 2]),
        # ({"list": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]}, "list.select(a)", [1, 2, 3, 4]),
    ],
)
def filtering_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"list_1": [1, 2, 3, 4], "list_2": [3, 5]}, "list_1.intersect([list_2])", [3]),
        ({"list_1": [1, 2, 3, 4], "list_2": [0, 10]}, "list_1.intersect(list_2)", []),
        ({}, "(1 | 2 | 3).intersect(2 | 4)", [2])
    ],
)
def subsetting_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"a": 42}, "a > 42", [False]),
        ({"a": 42}, "a >= 42", [True]),
        ({"a": 42}, "a < 42", [False]),
        ({"a": 42}, "a <= 42", [True]),
        ({"a": 42}, "a != 41.0", [True]),
        ({"a": 42}, "a != 42.0", [False]),
        ({"a": 42}, "a != 42", [False]),
        ({"a": 42}, "a = 41.0", [False]),
        ({"a": 42}, "a = 42", [True]),
        ({"a": 42}, "a = 42.0", [True]),
        ({"a": 42}, "a ~ 42", [True]),
        ({"a": 42}, "a !~ 42", [False]),
    ],
)
def equality_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        # list
        ({"a": [1, 2, 3]}, "a.exists()", [True]),
        ({"a": [3, 4, 5]}, "a.exists($this > 1.0)", [True]),
        ({"a": [0, 1]}, "a.exists($this > 1.0)", [False]),
        ({"a": []}, "a.empty()", [True]),
        ({"a": True}, "a.not()", [False]),
        ({"a": [1, 2, 3], "b": [1, 2, 3, 4]}, "a.subsetOf(b)", [True]),
        ({"a": [1, 2, 3], "b": [1, 2, 3, 4]}, "b.subsetOf(a)", [False]),
        ({"a": [1, 2, 3], "b": [1, 2, 3, 4]}, "a.supersetOf(b)", [False]),
        ({"a": [1, 2, 3], "b": [1, 2, 3, 4]}, "b.supersetOf(a)", [True]),
        ({"a": [0, 1.0, 2]}, "a.all($this > 0)", [False]),
        ({"a": [0, 1, 2]}, "a.all($this >= 0)", [True]),
        # true
        ({"a": [True, True]}, "a.allTrue()", [True]),
        ({"a": [True, False]}, "a.allTrue()", [False]),
        ({"a": [False, False]}, "a.allTrue()", [False]),
        ({"a": [True, True]}, "a.anyTrue()", [True]),
        ({"a": [True, False]}, "a.anyTrue()", [True]),
        ({"a": [False, False]}, "a.anyTrue()", [False]),
        # false
        ({"a": [True, True]}, "a.allFalse()", [False]),
        ({"a": [True, False]}, "a.allFalse()", [False]),
        ({"a": [False, False]}, "a.allFalse()", [True]),
        ({"a": [True, True]}, "a.anyFalse()", [False]),
        ({"a": [True, False]}, "a.anyFalse()", [True]),
        ({"a": [False, False]}, "a.anyFalse()", [True]),
    ],
)
def existence_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({}, "iif(true, 'a', 'b')", ["a"]),
        ({"a": {"b": [1, 2, 3]}}, "a.b.trace()", [1, 2, 3]),
        ({"a": True}, "a.toInteger()", [1]),
        ({"a": False}, "a.toInteger()", [0]),
        ({"a": True}, "a.toDecimal()", [1.0]),
        ({"a": False}, "a.toDecimal()", [0]),
        ({"a": False}, "a.toString()", ["False"]),
        ({"a": 101.99}, "a.toString()", ["101.99"]),
    ],
)
def misc_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected

def time_functions_test():
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    tz_offset = datetime.timedelta(hours=3)
    with freeze_time(lambda: datetime.datetime(year=2020, month=8, day=20, hour=17, minute=52, second=15)):
        assert datetime.datetime.fromisoformat(evaluate({}, 'now()')[0]).timestamp() == datetime.datetime.now().replace(tzinfo=local_tz).timestamp()
        assert evaluate({}, 'today()') == ["2020-08-20"]
        assert evaluate({}, 'timeOfDay()') == ["17:52:15"]

def now_function_test():
    with freeze_time(lambda: datetime.datetime(2020, 8, 20)) as frozen_datetime:
        old_now_value = evaluate({}, 'now()')
        frozen_datetime.tick(1.0)
        new_now_value = evaluate({}, 'now()')

    assert old_now_value != new_now_value


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"numbers": [1, 2], "booleans": [True]}, "numbers | booleans", [1, 2, True]),
        (
            {"numbers": [1, 2], "booleans": [True, False]},
            "numbers.combine(booleans)",
            [1, 2, True, False],
        ),
    ],
)
def combining_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"a": {"b": {"c": [1, 2, 3]}}}, "a.children()", [{"c": [1, 2, 3]}]),
        ({"a": {"b": {"c": [1, 2, 3]}}}, "a.children().children()", [1, 2, 3]),
        ({"a": {"b": [1, 2, 3]}}, "a.descendants()", [1, 2, 3]),
        (
            {"a": {"b": {"c": [1, 2, 3]}}},
            "a.descendants()",
            [{"c": [1, 2, 3]}, 1, 2, 3],
        ),
    ],
)
def path_functions_test(resource, path, expected):
    assert evaluate(resource, path) == expected


@pytest.mark.parametrize(
    ("resource", "path", "expected"),
    [
        ({"a": "lorem ipsum"}, "a.contains('sum')", [True]),
        ({"a": "lorem ipsum"}, dsl.a.contains('sum'), [True]),
    ],
)
def convert_dsl_path_test(resource, path, expected):
    assert evaluate(resource, path) == expected
