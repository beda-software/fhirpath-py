import json
import math
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

"""
Adds the math functions to the given FHIRPath engine.
"""


def isEmpty(x):
    if util.isNumber(x):
        return False
    return len(x) == 0


def ensureNumberSingleton(x):
    data = util.valData(x)
    if not util.isNumber(data):
        if not isinstance(data, list) or len(data) != 1:
            raise Exception("Expected list with number, but got " + json.dumps(data))

        value = util.valData(data[0])

        if not util.isNumber(value):
            raise Exception("Expected number, but got " + json.dumps(x))

        return value
    return data


def amp(x="", y=""):
    return x + y


def minus(xs, ys):
    if len(xs) == 1 and len(ys) == 1:
        x = util.valData(xs[0])
        y = util.valData(ys[0])

        if util.isNumber(x) and util.isNumber(y):
            return x - y

        if isinstance(x, nodes.FP_TimeBase) and isinstance(y, nodes.FP_Quantity):
            return x.plus(nodes.FP_Quantity(-y.value, y.unit))

    raise Exception("Cannot " + json.dumps(xs) + " - " + json.dumps(ys))


def mul(x, y):
    return x * y


def div(x, y):
    return x / y


def intdiv(x, y):
    return int(x / y)


def mod(x, y):
    return x % y


# HACK: for only polymorphic function
# Actually, "minus" is now also polymorphic
def plus(xs, ys):
    if len(xs) != 1 or len(ys) != 1:
        raise Exception("Cannot " + json.dumps(xs) + " + " + json.dumps(ys))

    x = util.valData(xs[0])
    y = util.valData(ys[0])

    """
  In the future, this and other functions might need to return ResourceNode
  to preserve the type information (integer vs decimal, and maybe decimal
  vs string if decimals are represented as strings), in order to support
  "as" and "is", but that support is deferred for now.
  """
    if type(x) == str and type(y) == str:
        return x + y

    if util.isNumber(x) and util.isNumber(y):
        return x + y

    if isinstance(x, nodes.FP_TimeBase) and isinstance(y, nodes.FP_Quantity):
        return x.plus(y)


def abs(x):
    if isEmpty(x):
        return []
    num = ensureNumberSingleton(x)
    return math.fabs(num)


def ceiling(x):
    if isEmpty(x):
        return []
    num = ensureNumberSingleton(x)
    return math.ceil(num)


def exp(x):
    if isEmpty(x):
        return []
    num = ensureNumberSingleton(x)
    return math.exp(num)


def floor(x):
    if isEmpty(x):
        return []
    num = ensureNumberSingleton(x)
    return math.floor(num)


def ln(x):
    if isEmpty(x):
        return []

    num = ensureNumberSingleton(x)
    return math.log(num)


def log(x, base):
    if isEmpty(x) or isEmpty(base):
        return []

    num = ensureNumberSingleton(x)
    num2 = ensureNumberSingleton(base)

    return math.log(num, num2)


def power(x, degree):
    if isEmpty(x) or isEmpty(degree):
        return []

    num = ensureNumberSingleton(x)
    num2 = ensureNumberSingleton(degree)

    if num < 0 or math.floor(num2) != num2:
        return []

    return math.pow(num, num2)


def rround(x, acc):
    if isEmpty(x):
        return []

    num = ensureNumberSingleton(x)
    if isEmpty(acc):
        return round(num)

    num2 = ensureNumberSingleton(acc)
    degree = math.pow(10, num2)

    return round(num * degree) / degree


def sqrt(x):
    if isEmpty(x):
        return []

    num = ensureNumberSingleton(x)
    if num < 0:
        return []

    return math.sqrt(num)


def truncate(x):
    if isEmpty(x):
        return []
    num = ensureNumberSingleton(x)
    return math.trunc(num)
