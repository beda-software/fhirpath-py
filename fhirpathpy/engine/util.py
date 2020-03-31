from functools import reduce
from fhirpathpy.engine.nodes import ResourceNode


def valData(value):
    if isinstance(value, ResourceNode):
        return value.data
    return value


def isNumber(value):
    return isinstance(value, (int, float, complex)) and not isinstance(value, bool)


def isCapitalized(x):
    return isinstance(x, list) and x[0] == x[0].upper()


def isEmpty(x):
    return isinstance(x, list) and len(x) == 0


def isSome(x):
    return x is not None and not isEmpty(x)


def isNullable(x):
    return x is None or isEmpty(x)


def isTrue(x):
    return x == True or isinstance(x, list) and len(x) == 1 and x[0] == True


def arraify(x):
    if isinstance(x, list):
        return x
    if isSome(x):
        return [x]
    return []


def flatten(x):
    def func(acc, x):
        if isinstance(x, list):
            acc = acc + x
        else:
            acc.append(x)

        return acc

    return reduce(func, x, [])
