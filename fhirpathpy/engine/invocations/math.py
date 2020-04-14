import math
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

"""
Adds the math functions to the given FHIRPath engine.
"""


def is_empty(x):
    if util.is_number(x):
        return False
    return util.is_empty(x)


def ensure_number_singleton(x):
    data = util.get_data(x)
    if not util.is_number(data):
        if not isinstance(data, list) or len(data) != 1:
            raise Exception("Expected list with number, but got " + str(data))

        value = util.get_data(data[0])

        if not util.is_number(value):
            raise Exception("Expected number, but got " + str(x))

        return value
    return data


def amp(ctx, x="", y=""):
    return x + y


def minus(ctx, xs, ys):
    if len(xs) == 1 and len(ys) == 1:
        x = util.get_data(xs[0])
        y = util.get_data(ys[0])

        if util.is_number(x) and util.is_number(y):
            return x - y

        if isinstance(x, nodes.FP_TimeBase) and isinstance(y, nodes.FP_Quantity):
            return x.plus(nodes.FP_Quantity(-y.value, y.unit))

    raise Exception("Cannot " + str(xs) + " - " + str(ys))


def mul(ctx, x, y):
    return x * y


def div(ctx, x, y):
    return x / y


def intdiv(ctx, x, y):
    return int(x / y)


def mod(ctx, x, y):
    return x % y


# HACK: for only polymorphic function
# Actually, "minus" is now also polymorphic
def plus(ctx, xs, ys):
    if len(xs) != 1 or len(ys) != 1:
        raise Exception("Cannot " + str(xs) + " + " + str(ys))

    x = util.get_data(xs[0])
    y = util.get_data(ys[0])

    """
    In the future, this and other functions might need to return ResourceNode
    to preserve the type information (integer vs decimal, and maybe decimal
    vs string if decimals are represented as strings), in order to support
    "as" and "is", but that support is deferred for now.
    """
    if type(x) == str and type(y) == str:
        return x + y

    if util.is_number(x) and util.is_number(y):
        return x + y

    if isinstance(x, nodes.FP_TimeBase) and isinstance(y, nodes.FP_Quantity):
        return x.plus(y)


def abs(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return math.fabs(num)


def ceiling(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return math.ceil(num)


def exp(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return math.exp(num)


def floor(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return math.floor(num)


def ln(ctx, x):
    if is_empty(x):
        return []

    num = ensure_number_singleton(x)
    return math.log(num)


def log(ctx, x, base):
    if is_empty(x) or is_empty(base):
        return []

    num = ensure_number_singleton(x)
    num2 = ensure_number_singleton(base)

    return math.log(num, num2)


def power(ctx, x, degree):
    if is_empty(x) or is_empty(degree):
        return []

    num = ensure_number_singleton(x)
    num2 = ensure_number_singleton(degree)

    if num < 0 or math.floor(num2) != num2:
        return []

    return math.pow(num, num2)


def rround(ctx, x, acc):
    if is_empty(x):
        return []

    num = ensure_number_singleton(x)
    if is_empty(acc):
        return round(num)

    num2 = ensure_number_singleton(acc)
    degree = math.pow(10, num2)

    return round(num * degree) / degree


def sqrt(ctx, x):
    if is_empty(x):
        return []

    num = ensure_number_singleton(x)
    if num < 0:
        return []

    return math.sqrt(num)


def truncate(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return math.trunc(num)
