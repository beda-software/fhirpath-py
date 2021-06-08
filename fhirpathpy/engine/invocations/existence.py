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

    if type(data) == bool:
        return not data

    return []


def exists_macro(ctx, coll, expr=None):
    vec = coll
    if expr is not None:
        return exists_macro(ctx, filtering.where_macro(ctx, coll, expr))

    return not util.is_empty(vec)


def all_macro(ctx, colls, expr):
    for coll in colls:
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
    if all([isinstance(v, nodes.ResourceNode) for v in x]):
        data = [v.data for v in x]

        unique = util.uniq(data)

        return [nodes.ResourceNode.create_node(item) for item in unique]

    return util.uniq(x)

def isdistinct_fn(ctx, x):
    return [len(x) == len(distinct_fn(ctx, x))]
