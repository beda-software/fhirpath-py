from decimal import Decimal
import json
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

"""
This file holds code to hande the FHIRPath Math functions.
"""
DATETIME_NODES_LIST = (nodes.FP_DateTime, nodes.FP_Time)


def equality(ctx, x, y):
    if util.is_empty(x) or util.is_empty(y):
        return False

    if type(x[0]) in DATETIME_NODES_LIST or type(y[0]) in DATETIME_NODES_LIST:
        return datetime_equality(ctx, x, y)

    if len(x) != len(y):
        return False

    a = util.parse_value(x[0])
    b = util.parse_value(y[0])

    if (
        isinstance(a, nodes.FP_Quantity)
        and isinstance(b, nodes.FP_Quantity)
        and getattr(b, "unit", None) in nodes.FP_Quantity.mapUCUMCodeToTimeUnits.values()
    ):
        return a.deep_equal(b)

    return a == b


def normalize_string(s):
    return " ".join(s.lower().split())


def decimal_places(a):
    d = Decimal(str(a))
    match = f"{d:.{abs(d.as_tuple().exponent)}f}".rstrip("0").rstrip(".").split(".")
    return len(match[1]) if len(match) > 1 else 0


def round_to_decimal_places(a, n):
    rounding_format = Decimal("10") ** -n
    return Decimal(a).quantize(rounding_format)


def is_equivalent(a, b):
    precision = min(decimal_places(a), decimal_places(b))
    if precision == 0:
        return round(a) == round(b)
    else:
        return round_to_decimal_places(a, precision) == round_to_decimal_places(b, precision)


def equivalence(ctx, x, y):
    if util.is_empty(x) and util.is_empty(y):
        return True

    if util.is_empty(x) or util.is_empty(y):
        return False

    a = util.get_data(x[0])
    b = util.get_data(y[0])

    if type(a) in DATETIME_NODES_LIST or type(b) in DATETIME_NODES_LIST:
        return datetime_equality(ctx, x, y)

    if isinstance(a, str) and isinstance(b, str):
        return normalize_string(a) == normalize_string(b)

    if isinstance(a, Decimal) or isinstance(b, Decimal):
        return is_equivalent(a, b)

    x_val = util.parse_value(x[0])
    y_val = util.parse_value(y[0])

    if isinstance(x_val, nodes.FP_Quantity) and isinstance(y_val, nodes.FP_Quantity):
        return x_val.deep_equal(y_val)

    if isinstance(a, (dict, list)) and isinstance(b, (dict, list)):
        def deep_equal(a, b):
            if isinstance(a, dict) and isinstance(b, dict):
                if a.keys() != b.keys():
                    return False
                return all(deep_equal(a[key], b[key]) for key in a)
            elif isinstance(a, list) and isinstance(b, list):
                return len(a) == len(b) and all(
                    deep_equal(x, y) for x, y in zip(sorted(a), sorted(b))
                )
            elif isinstance(a, str) and isinstance(b, str):
                return normalize_string(a) == normalize_string(b)
            elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return abs(a - b) < 0.5
            else:
                return a == b

        return deep_equal(a, b)

    return x == y


def datetime_equality(ctx, x, y):
    datetime_x = x[0]
    datetime_y = y[0]
    if datetime_x is None or datetime_y is None:
        return None
    if type(datetime_x) not in DATETIME_NODES_LIST:
        v_x = util.get_data(datetime_x)
        datetime_x = nodes.FP_DateTime(v_x) or nodes.FP_Time(v_x)
    if type(datetime_y) not in DATETIME_NODES_LIST:
        v_y = util.get_data(datetime_y)
        datetime_y = nodes.FP_DateTime(v_y) or nodes.FP_Time(v_y)
    return datetime_x.equals(datetime_y)


def equal(ctx, a, b):
    equality_result = equality(ctx, a, b)
    return util.arraify(equality_result)


def unequal(ctx, a, b):
    equality_result = equality(ctx, a, b)
    unequality_result = None if equality_result is None else not equality_result
    return util.arraify(unequality_result)


def equival(ctx, a, b):
    equivalence_result = equivalence(ctx, a, b)
    return util.arraify(equivalence_result, instead_none=False)


def unequival(ctx, a, b):
    equivalence_result = equivalence(ctx, a, b)
    unequivalence_result = None if equivalence_result is None else not equivalence_result
    return util.arraify(unequivalence_result, instead_none=True)


def check_length(value):
    if len(value) > 1:
        raise Exception(
            "Was expecting no more than one element but got "
            + json.dumps(value)
            + ". Singleton was expected"
        )


def remove_duplicate_extension(list):
    """
    This is a temporary solution for cases where the list contains 2 items with the same key,
    like birthDate and _birthDate. Needs to be fixed to a better solution.
    """
    if len(list) == 2 and isinstance(list[1], nodes.ResourceNode) and "extension" in list[1].data:
        return list[:1]
    return list


def typecheck(a, b):
    """
    Checks that the types of a and b are suitable for comparison in an
    inequality expression.  It is assumed that a check has already been made
    that there is at least one value in a and b.

    Parameters:
    a (list) - the left side of the inequality expression (which should be an array of one value)
    b (list) -  the right side of the inequality expression (which should be an array of one value)

    returns the singleton values of the arrays a, and b.  If one was an FP_Type and the other was convertible, the coverted value will be retureed
    """
    rtn = None

    a = remove_duplicate_extension(a)
    b = remove_duplicate_extension(b)

    check_length(a)
    check_length(b)

    a = util.get_data(a[0])
    b = util.get_data(b[0])

    lClass = a.__class__
    rClass = b.__class__

    areNumbers = util.is_number(a) and util.is_number(b)

    if lClass != rClass and not areNumbers:
        d = None

        # TODO refactor
        if lClass == str and (rClass == nodes.FP_DateTime or rClass == nodes.FP_Time):
            d = nodes.FP_DateTime(a) or nodes.FP_Time(a)
            if d is not None:
                rtn = [d, b]
        elif rClass == str and (lClass == nodes.FP_DateTime or lClass == nodes.FP_Time):
            d = nodes.FP_DateTime(b) or nodes.FP_Time(b)
            if d is not None:
                rtn = [a, d]

        if rtn is None:
            raise Exception(
                'Type of "'
                + str(a)
                + '" ('
                + lClass.__name__
                + ') did not match type of "'
                + str(b)
                + '" ('
                + rClass.__name__
                + "). InequalityExpression"
            )

    if rtn is not None:
        return rtn

    return [a, b]


def lt(ctx, a, b):
    if len(a) == 0 or len(b) == 0:
        return []
    if a[0] is None or b[0] is None:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        if (
            isinstance(a0, nodes.FP_TimeBase)
            and a0.compare(b0) is None
            and a0._precision != b0._precision
        ):
            return None
        return a0.compare(b0) == -1

    return a0 < b0


def gt(ctx, a, b):
    if len(a) == 0 or len(b) == 0:
        return []
    if a[0] is None or b[0] is None:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        if (
            isinstance(a0, nodes.FP_TimeBase)
            and a0.compare(b0) is None
            and a0._precision != b0._precision
        ):
            return None
        return a0.compare(b0) == 1

    return a0 > b0


def lte(ctx, a, b):
    if len(a) == 0 or len(b) == 0:
        return []
    if a[0] is None or b[0] is None:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        if (
            isinstance(a0, nodes.FP_TimeBase)
            and a0.compare(b0) is None
            and a0._precision != b0._precision
        ):
            return None
        return a0.compare(b0) <= 0

    return a0 <= b0


def gte(ctx, a, b):
    if len(a) == 0 or len(b) == 0:
        return []
    if a[0] is None or b[0] is None:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        if (
            isinstance(a0, nodes.FP_TimeBase)
            and a0.compare(b0) is None
            and a0._precision != b0._precision
        ):
            return None
        return a0.compare(b0) >= 0

    return a0 >= b0
