import numbers
import fhirpathpy.engine.util as util

# Contains the FHIRPath Filtering and Projection functions.
# (Section 5.2 of the FHIRPath 1.0.0 specification).

"""
 Adds the filtering and projection functions to the given FHIRPath engine.
"""


def where_macro(data, expr):
    if not isinstance(data, list):
        return []

    filtered = list(filter(lambda x: expr(x)[0], data))
    return util.flatten(filtered)


def select_macro(data, expr):
    if not isinstance(data, list):
        return []

    mapped = list(filter(lambda x: expr(x), data))

    return util.flatten(mapped)


def repeat_macro(data, expr):
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
def single_fn(x):
    if len(x) == 1:
        return x

    if len(x) == 0:
        return []

    # TODO: should throw error?
    return {"$status": "error", "$error": "Expected single"}


def first_fn(x):
    return x[0]


def last_fn(x):
    return x[-1]


def tail_fn(x):
    return x[1:]


def take_fn(x, n):
    return x[: int(n)]


def skip_fn(x, n):
    return x[int(n) :]


# TODO test
def check_fhir_type(x, tp):
    if type(x) == tp:
        return True

    if tp == "integer":
        return int(x) == x

    if tp == "decimal":
        return isinstance(x, numbers.Number)

    return False


def of_type_fn(coll, type):
    return list(filter(lambda x: check_fhir_type(util.get_data(x), type), coll))
