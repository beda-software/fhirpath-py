import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

"""
This file holds code to hande the FHIRPath Math functions.
"""


def equality(x, y):
    if util.isEmpty(x) or util.isEmpty(y):
        return False

    return x == y


def equivalence(x, y):
    if util.isEmpty(x) and util.isEmpty(y):
        return True

    if util.isEmpty(x) or util.isEmpty(y):
        return False

    return x == y


def equal(a, b):
    return [equality(a, b)]


def unequal(a, b):
    return [not equality(a, b)]


def equival(a, b):
    return [equivalence(a, b)]


def unequival(a, b):
    return [not equivalence(a, b)]


def checkLength(value):
    if len(value) > 1:
        raise Exception(
            "Was expecting no more than one element but got "
            + json.dumps(a)
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

    checkLength(a)
    checkLength(b)

    a = util.valData(a[0])
    b = util.valData(b[0])

    lClass = a.__class__
    rClass = b.__class__

    if lClass != rClass:
        d = None

        # TODO refactor
        if lClass == str and (rClass == nodes.FP_DateTime or rClass == nodes.FP_Time):
            d = rClass.checkString(a)  # TODO
            if d is not None:
                rtn = [d, b]
        elif rClass == str and (lClass == nodes.FP_DateTime or lClass == nodes.FP_Time):
            d = lClass.checkString(b)  # TODO
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


def lt(a, b):
    if len(a) == 0 or len(b) == 0:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) == -1

    return a0 < b0


def gt(a, b):
    if len(a) == 0 or len(b) == 0:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) == 1

    return a0 > b0


def lte(a, b):
    if len(a) == 0 or len(b) == 0:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) <= 0

    return a0 <= b0


def gte(a, b):
    if len(a) == 0 or len(b) == 0:
        return []

    vals = typecheck(a, b)
    a0 = vals[0]
    b0 = vals[1]

    if isinstance(a0, nodes.FP_Type):
        return a0.compare(b0) >= 0

    return a0 >= b0
