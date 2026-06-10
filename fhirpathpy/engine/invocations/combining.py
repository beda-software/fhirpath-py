from fhirpathpy.engine import util
from fhirpathpy.engine.invocations import existence

"""
This file holds code to hande the FHIRPath Combining functions
"""


def union_op(ctx, coll1, coll2):
    return existence.distinct_fn(ctx, coll1 + coll2)


def combine_fn(ctx, coll1, coll2):
    return coll1 + coll2


def exclude_fn(ctx, coll1, coll2):
    return [element for element in coll1 if element not in coll2]


def coalesce_fn(ctx, data, *exprs):
    for expr in exprs:
        result = expr(data)
        if not util.is_empty(result):
            return result
    return []
