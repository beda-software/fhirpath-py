from decimal import Decimal
from fhirpathpy.engine.invocations.equality import remove_duplicate_extension
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
    if isinstance(data, float):
        data = Decimal(data)

    if not util.is_number(data):
        if not isinstance(data, list) or len(data) != 1:
            raise Exception("Expected list with number, but got " + str(data))

        value = util.get_data(data[0])

        if isinstance(value, float):
            value = Decimal(value)

        if not util.is_number(value):
            raise Exception("Expected number, but got " + str(x))

        return value
    return data


def amp(ctx, x="", y=""):
    if isinstance(x, list) and not x:
        x = ""
    if isinstance(y, list) and not y:
        y = ""
    return x + y


def minus(ctx, xs_, ys_):
    xs = remove_duplicate_extension(xs_)
    ys = remove_duplicate_extension(ys_)

    if len(xs) != 1 or len(ys) != 1:
        raise Exception("Cannot " + str(xs) + " - " + str(ys))

    x = util.get_data(util.val_data_converted(xs[0]))
    y = util.get_data(util.val_data_converted(ys[0]))

    if util.is_number(x) and util.is_number(y):
        return x - y

    if isinstance(x, nodes.FP_TimeBase) and isinstance(y, nodes.FP_Quantity):
        return x.plus(nodes.FP_Quantity(-y.value, y.unit))

    if isinstance(x, str) and isinstance(y, nodes.FP_Quantity):
        x_ = nodes.FP_TimeBase.get_match_data(x)
        if x_ is not None:
            return x_.plus(nodes.FP_Quantity(-y.value, y.unit))

    raise Exception("Cannot " + str(xs) + " - " + str(ys))


def mul(ctx, x, y):
    return x * y


def div(ctx, x, y):
    if y == 0:
        return []
    return x / y


def intdiv(ctx, x, y):
    if y == 0:
        return []
    return int(x / y)


def mod(ctx, x, y):
    if y == 0:
        return []

    return x % y


# HACK: for only polymorphic function
# Actually, "minus" is now also polymorphic
def plus(ctx, xs_, ys_):
    xs = remove_duplicate_extension(xs_)
    ys = remove_duplicate_extension(ys_)

    if len(xs) != 1 or len(ys) != 1:
        raise Exception("Cannot " + str(xs) + " + " + str(ys))

    x = util.get_data(util.val_data_converted(xs[0]))
    y = util.get_data(util.val_data_converted(ys[0]))

    """
    In the future, this and other functions might need to return ResourceNode
    to preserve the type information (integer vs decimal, and maybe decimal
    vs string if decimals are represented as strings), in order to support
    "as" and "is", but that support is deferred for now.
    """
    if isinstance(x, str) and isinstance(y, str):
        return x + y

    if util.is_number(x) and util.is_number(y):
        return x + y

    if isinstance(x, nodes.FP_TimeBase) and isinstance(y, nodes.FP_Quantity):
        return x.plus(y)

    if isinstance(x, str) and isinstance(y, nodes.FP_Quantity):
        x_ = nodes.FP_TimeBase.get_match_data(x)
        if x_ is not None:
            return x_.plus(y)

    raise Exception("Cannot " + str(xs) + " + " + str(ys))


def abs(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return Decimal(num).copy_abs()


def ceiling(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return Decimal(num).to_integral_value(rounding="ROUND_CEILING")


def exp(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return Decimal(num).exp()


def floor(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return Decimal(num).to_integral_value(rounding="ROUND_FLOOR")


def ln(ctx, x):
    if is_empty(x):
        return []

    num = ensure_number_singleton(x)
    return Decimal(num).ln()


def log(ctx, x, base):
    if is_empty(x) or is_empty(base):
        return []

    num = Decimal(ensure_number_singleton(x))
    num2 = Decimal(ensure_number_singleton(base))

    return (num.ln() / num2.ln()).quantize(Decimal("1.000000000000000"))


def power(ctx, x, degree):
    if is_empty(x) or is_empty(degree):
        return []

    num = Decimal(ensure_number_singleton(x))
    num2 = Decimal(ensure_number_singleton(degree))

    if num < 0 or num2.to_integral_value(rounding="ROUND_FLOOR") != num2:
        return []

    return pow(num, num2)


def rround(ctx, x, acc):
    if is_empty(x):
        return []

    num = Decimal(ensure_number_singleton(x))
    if is_empty(acc):
        return round(num)

    num2 = ensure_number_singleton(acc)
    degree = 10 ** Decimal(num2)

    return round(num * degree) / degree


def sqrt(ctx, x):
    if is_empty(x):
        return []

    num = ensure_number_singleton(x)
    if num < 0:
        return []

    return Decimal(num).sqrt()


def truncate(ctx, x):
    if is_empty(x):
        return []
    num = ensure_number_singleton(x)
    return Decimal(num).to_integral_value(rounding="ROUND_DOWN")
