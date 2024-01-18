from decimal import Decimal
from fhirpathpy.engine.invocations import misc
from fhirpathpy.engine.invocations.misc import to_boolean
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes
import fhirpathpy.engine.invocations.filtering as filtering


"""
This file holds code to hande the FHIRPath Existence functions
(5.1 in the specification).
"""


def empty_fn(ctx, value):
    return util.is_empty(value)


def count_fn(ctx, value):
    if isinstance(value, list):
        return len(value)
    return 0


def not_fn(ctx, x):
    if len(x) != 1:
        return []

    data = util.get_data(x[0])
    data = misc.singleton(x, "Boolean")

    if isinstance(data, bool):
        return not data

    return []


def exists_macro(ctx, coll, expr=None):
    vec = coll
    if expr is not None:
        return exists_macro(ctx, filtering.where_macro(ctx, coll, expr))

    return not util.is_empty(vec)


def all_macro(ctx, colls, expr):
    for i, coll in enumerate(colls):
        ctx["$index"] = i
        if not util.is_true(expr(coll)):
            return [False]

    return [True]


def extract_boolean_value(data):
    value = util.get_data(data)
    if type(value) != bool:
        raise Exception("Found type '" + type(data) + "' but was expecting bool")
    return value


def all_true_fn(ctx, items):
    return [all(extract_boolean_value(item) for item in items)]


def any_true_fn(ctx, items):
    return [any(extract_boolean_value(item) for item in items)]


def all_false_fn(ctx, items):
    return [all(not extract_boolean_value(item) for item in items)]


def any_false_fn(ctx, items):
    return [any(not extract_boolean_value(item) for item in items)]


def subset_of(ctx, coll1, coll2):
    return all(item in coll2 for item in coll1)


def subset_of_fn(ctx, coll1, coll2):
    return [subset_of(ctx, coll1, coll2)]


def superset_of_fn(ctx, coll1, coll2):
    return [subset_of(ctx, coll2, coll1)]


def distinct_fn(ctx, x):
    conversion_factors = {
        "weeks": Decimal("604800000"),
        "'wk'": Decimal("604800000"),
        "week": Decimal("604800000"),
        "days": Decimal("86400000"),
        "'d'": Decimal("86400000"),
        "day": Decimal("86400000"),
        "hours": Decimal("3600000"),
        "'h'": Decimal("3600000"),
        "hour": Decimal("3600000"),
        "minutes": Decimal("60000"),
        "'min'": Decimal("60000"),
        "minute": Decimal("60000"),
        "seconds": Decimal("1000"),
        "'s'": Decimal("1000"),
        "second": Decimal("1000"),
        "milliseconds": Decimal("1"),
        "'ms'": Decimal("1"),
        "millisecond": Decimal("1"),
        "years": Decimal("12"),
        "'a'": Decimal("12"),
        "year": Decimal("12"),
        "months": Decimal("1"),
        "'mo'": Decimal("1"),
        "month": Decimal("1"),
    }

    if all(isinstance(v, nodes.ResourceNode) for v in x):
        data = [v.data for v in x]
        unique = util.uniq(data)
        return [nodes.ResourceNode.create_node(item) for item in unique]

    if all(isinstance(v, nodes.FP_Quantity) for v in x):
        converted_values = {}
        original_values = {}

        for interval in x:
            unit = interval.unit
            if unit in conversion_factors:
                converted_value = interval.value * conversion_factors[unit]
                if converted_value not in converted_values:
                    converted_values[converted_value] = interval.value
                    original_values[converted_value] = interval

        if len(converted_values) == 1:
            return [list(original_values.values())[0]]

        return [original_values[val] for val in util.uniq(converted_values.values())]

    return util.uniq(x)


def isdistinct_fn(ctx, x):
    return [len(x) == len(distinct_fn(ctx, x))]
