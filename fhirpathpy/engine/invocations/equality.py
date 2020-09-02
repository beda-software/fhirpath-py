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

    return x == y


def equivalence(ctx, x, y):
    if util.is_empty(x) and util.is_empty(y):
        return True

    if util.is_empty(x) or util.is_empty(y):
        return False

    if type(x[0]) in DATETIME_NODES_LIST or type(y[0]) in DATETIME_NODES_LIST:
        return datetime_equality(ctx, x, y)

    return x == y


def datetime_equality(ctx, x, y):
    datetime_x = x[0]
    datetime_y = y[0]
    if type(datetime_x) not in DATETIME_NODES_LIST:
        datetime_x = nodes.FP_DateTime(datetime_x) or nodes.FP_Time(datetime_x)
    if type(datetime_y) not in DATETIME_NODES_LIST:
        datetime_y = nodes.FP_DateTime(datetime_y) or nodes.FP_Time(datetime_y)
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

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) == -1

    return a0 < b0


def gt(ctx, a, b):
    if len(a) == 0 or len(b) == 0:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) == 1

    return a0 > b0


def lte(ctx, a, b):
    if len(a) == 0 or len(b) == 0:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) <= 0

    return a0 <= b0


def gte(ctx, a, b):
    if len(a) == 0 or len(b) == 0:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) >= 0

    return a0 >= b0
