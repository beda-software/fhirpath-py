import json
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes
import fhirpathpy.engine.invocations.filtering as filtering

"""
This file holds code to hande the FHIRPath Existence functions 
(5.1 in the specification).
"""


def emptyFn(value):
    return util.isEmpty(value)


def countFn(value):
    if isinstance(value, list):
        return len(value)
    return 0


def notFn(x):
    if len(x) != 1:
        return []

    data = util.valData(x[0])

    if type(data) == bool:
        return not data

    return []


def existsMacro(coll, expr=None):
    vec = coll
    if expr is not None:
        return existsMacro(filtering.whereMacro(coll, expr))

    return not util.isEmpty(vec)


def allMacro(colls, expr):
    for coll in colls:
        if not util.isTrue(expr(coll)):
            return [False]

    return [True]


def extractBooleanValue(data):
    value = util.valData(data)
    if type(value) != bool:
        raise Exception("Found type '" + type(data) + "' but was expecting bool")
    return value


def allTrueFn(items):
    return [all(extractBooleanValue(item) for item in items)]


def anyTrueFn(items):
    return [any(extractBooleanValue(item) for item in items)]


def allFalseFn(items):
    return [all(not extractBooleanValue(item) for item in items)]


def anyFalseFn(items):
    return [any(not extractBooleanValue(item) for item in items)]


def subsetOf(coll1, coll2):
    return all(item in coll2 for item in coll1)


def subsetOfFn(coll1, coll2):
    return [subsetOf(coll1, coll2)]


def supersetOfFn(coll1, coll2):
    return [subsetOf(coll2, coll1)]


def distinctFn(x):
    return list(set(x))


def isDistinctFn(x):
    return [len(x) == len(distinctFn(x))]
