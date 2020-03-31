import numbers
import fhirpathpy.engine.util as util

# Contains the FHIRPath Filtering and Projection functions.
# (Section 5.2 of the FHIRPath 1.0.0 specification).

"""
 Adds the filtering and projection functions to the given FHIRPath engine.
"""


def whereMacro(data, expr):
    if not isinstance(data, list):
        return []

    filtered = list(filter(lambda x: expr(x)[0], data))
    return util.flatten(filtered)


def selectMacro(data, expr):
    if not isinstance(data, list):
        return []

    mapped = list(filter(lambda x: expr(x), data))

    return util.flatten(mapped)


def repeatMacro(data, expr):
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
def singleFn(x):
    if len(x) == 1:
        return x

    if len(x) == 0:
        return []

    # TODO: should throw error?
    return {"$status": "error", "$error": "Expected single"}


def firstFn(x):
    return x[0]


def lastFn(x):
    return x[-1]


def tailFn(x):
    return x[1:]


def takeFn(x, n):
    return x[: int(n)]


def skipFn(x, n):
    return x[int(n) :]


# TODO test
def checkFHIRType(x, tp):
    if type(x) == tp:
        return True

    if tp == "integer":
        return int(x) == x

    if tp == "decimal":
        return isinstance(x, numbers.Number)

    return False


def ofTypeFn(coll, type):
    return list(filter(lambda x: checkFHIRType(util.valData(x), type), coll))
