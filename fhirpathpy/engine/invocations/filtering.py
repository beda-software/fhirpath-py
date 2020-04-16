import numbers
import fhirpathpy.engine.util as util

# Contains the FHIRPath Filtering and Projection functions.
# (Section 5.2 of the FHIRPath 1.0.0 specification).

"""
 Adds the filtering and projection functions to the given FHIRPath engine.
"""


def check_macro_expr(expr, x):
    result = expr(x)
    if len(result) > 0:
        return expr(x)[0]

    return False


def where_macro(ctx, data, expr):
    if not isinstance(data, list):
        return []

    return util.flatten([x for x in data if check_macro_expr(expr, x)])


def select_macro(ctx, data, expr):
    if not isinstance(data, list):
        return []

    return util.flatten([expr(x) for x in data])


def repeat_macro(ctx, data, expr):
    if not isinstance(data, list):
        return []

    res = []
    items = data

    next = None
    lres = None

    while len(items) != 0:
        next = items[0]
        items = items[1:]
        lres = expr(next)
        if lres:
            res = res + lres
            items = items + lres

    return res


# TODO: behavior on object?
def single_fn(ctx, x):
    if len(x) == 1:
        return x

    if len(x) == 0:
        return []

    # TODO: should throw error?
    return {"$status": "error", "$error": "Expected single"}


def first_fn(ctx, x):
    if len(x) == 0:
        return []
    return x[0]


def last_fn(ctx, x):
    if len(x) == 0:
        return []
    return x[-1]


def tail_fn(ctx, x):
    if len(x) == 0:
        return []
    return x[1:]


def take_fn(ctx, x, n):
    if len(x) == 0:
        return []
    return x[: int(n)]


def skip_fn(ctx, x, n):
    if len(x) == 0:
        return []
    return x[int(n) :]


def check_fhir_type(ctx, x, tp):
    if tp == "string" and type(x) == str:
        return True

    if tp == "boolean" and type(x) == bool:
        return True

    if tp == "object":
        return isinstance(x, dict)

    if tp == "integer" and type(x) == int:
        return True

    if tp == "decimal" and (type(x) == int or type(x) == float):
        return True

    return False


def of_type_fn(ctx, coll, tp):
    return list(filter(lambda x: check_fhir_type(ctx, util.get_data(x), tp), coll))
