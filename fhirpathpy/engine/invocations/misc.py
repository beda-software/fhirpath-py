import re
import json
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

# This file holds code to hande the FHIRPath Existence functions (5.1 in the
# specification).

intRegex = re.compile(r"^[+-]?\d+$")
numRegex = re.compile(r"^[+-]?\d+(\.\d+)?$")


def iifMacro(data, cond, ok, fail):
    if util.isTrue(cond(data)):
        return ok(data)

    return fail(data)


def traceFn(x, label=""):
    # print("TRACE:[" + label + "]", json.dumps(x))
    return x


def toInteger(coll):
    if len(coll) != 1:
        return []

    value = util.valData(coll[0])

    if value == False:
        return 0

    if value == True:
        return 1

    if util.isNumber(value):
        if int(value) == value:
            return value

        return []

    if str(value):
        if re.match(intRegex, value) is not None:
            return int(value)

        raise Exception("Could not convert to ineger: " + value)

    return []


def toDecimal(coll):
    if len(coll) != 1:
        return []

    value = util.valData(coll[0])

    if value == False:
        return 0

    if value == True:
        return 1.0

    if util.isNumber(value):
        return value

    if type(value) == str:
        if re.match(numRegex, value) is not None:
            return float(value)

        raise Exception("Could not convert to decimal: " + value)

    return []


def toString(coll):
    if len(coll) != 1:
        return []

    value = util.valData(coll[0])
    return str(value)


# Defines a function on engine called to+timeType (e.g., toDateTime, etc.).
# @param timeType The string name of a class for a time type (e.g. "FP_DateTime").


def toDateTime(coll):
    ln = len(coll)
    rtn = []
    if ln > 1:
        raise Exception("toDateTime called for a collection of length " + ln)

    if ln == 1:
        value = util.valData(coll[0])

        t = nodes.FP_DateTime.checkString(value)

        if t:
            rtn[0] = t

    return rtn


def toTime(coll):
    ln = len(coll)
    rtn = []
    if ln > 1:
        raise Exception("toTime called for a collection of length " + ln)

    if ln == 1:
        value = util.valData(coll[0])

        t = nodes.FP_Time.checkString(value)

        if t:
            rtn[0] = t

    return rtn
