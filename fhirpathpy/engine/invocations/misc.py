import re
from decimal import Decimal

import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes

# This file holds code to hande the FHIRPath Existence functions (5.1 in the
# specification).

intRegex = re.compile(r"^[+-]?\d+$")
numRegex = re.compile(r"^[+-]?\d+(\.\d+)?$")


def iif_macro(ctx, data, cond, ok, fail=None):
    if util.is_true(cond(data)):
        return ok(data)
    elif fail:
        return fail(data)
    else:
        return []


def trace_fn(ctx, x, label=""):
    print("TRACE:[" + label + "]", str(x))
    return x


def to_integer(ctx, coll):
    if len(coll) != 1:
        return []

    value = util.get_data(coll[0])

    if value == False:
        return 0

    if value == True:
        return 1

    if util.is_number(value):
        if int(value) == value:
            return value

        return []

    if isinstance(value, str):
        if re.match(intRegex, value) is not None:
            return int(value)

    return []


quantity_regex = re.compile(r"^((\+|-)?\d+(\.\d+)?)\s*(('[^']+')|([a-zA-Z]+))?$")
quantity_regex_map = {"value": 1, "unit": 5, "time": 6}


def to_quantity(ctx, coll, to_unit=None):
    result = None

    # Surround UCUM unit code in the to_unit parameter with single quotes
    if to_unit and not nodes.FP_Quantity.timeUnitsToUCUM.get(to_unit):
        to_unit = f"'{to_unit}'"

    if len(coll) > 1:
        raise Exception("Could not convert to quantity: input collection contains multiple items")
    elif len(coll) == 1:
        v = util.val_data_converted(coll[0])
        quantity_regex_res = None

        if isinstance(v, (int, Decimal)):
            result = nodes.FP_Quantity(v, "'1'")
        elif isinstance(v, nodes.FP_Quantity):
            result = v
        elif isinstance(v, bool):
            result = nodes.FP_Quantity(1 if v else 0, "'1'")
        elif isinstance(v, str):
            quantity_regex_res = quantity_regex.match(v)
            if quantity_regex_res:
                value = quantity_regex_res.group(quantity_regex_map["value"])
                unit = quantity_regex_res.group(quantity_regex_map["unit"])
                time = quantity_regex_res.group(quantity_regex_map["time"])

                if not time or nodes.FP_Quantity.timeUnitsToUCUM.get(time):
                    result = nodes.FP_Quantity(Decimal(value), unit or time or "'1'")

        if result and to_unit and result.unit != to_unit:
            result = nodes.FP_Quantity.conv_unit_to(result.unit, result.value, to_unit)

    return result if result else []


def to_decimal(ctx, coll):
    if len(coll) != 1:
        return []

    value = util.get_data(coll[0])

    if value is False:
        return Decimal(0)

    if value is True:
        return Decimal(1.0)

    if util.is_number(value):
        return Decimal(value)

    if isinstance(value, str):
        if re.match(numRegex, value) is not None:
            return Decimal(value)

    return []


def to_string(ctx, coll):
    if len(coll) != 1:
        return []

    value = util.get_data(coll[0])
    return str(value)


# Defines a function on engine called to+timeType (e.g., toDateTime, etc.).
# @param timeType The string name of a class for a time type (e.g. "FP_DateTime").


def to_date_time(ctx, coll):
    ln = len(coll)
    rtn = []
    if ln > 1:
        raise Exception("to_date_time called for a collection of length " + str(ln))

    if ln == 1:
        value = util.get_data(coll[0])

        dateTimeObject = nodes.FP_DateTime(value)

        if dateTimeObject:
            rtn.append(dateTimeObject)

    return util.get_data(rtn[0])


def to_time(ctx, coll):
    ln = len(coll)
    rtn = []
    if ln > 1:
        raise Exception("to_time called for a collection of length " + str(ln))

    if ln == 1:
        value = util.get_data(coll[0])

        timeObject = nodes.FP_Time(value)

        if timeObject:
            rtn.append(timeObject)

    return util.get_data(rtn[0])


def to_date(ctx, coll):
    ln = len(coll)
    rtn = []

    if ln > 1:
        raise Exception("to_date called for a collection of length " + str(ln))

    if ln == 1:
        value = util.get_data(coll[0])

        dateObject = nodes.FP_DateTime(value)

        if dateObject:
            rtn.append(dateObject)

    return util.get_data(rtn[0])


def create_converts_to_fn(to_function, _type):
    if isinstance(_type, str):
        def in_function(ctx, coll):
            if len(coll) != 1:
                return []
            return type(to_function(ctx, coll)).__name__ == _type
        return in_function

    def in_function(ctx, coll):
        if len(coll) != 1:
            return []

        return isinstance(to_function(ctx, coll), _type)

    return in_function


def to_boolean(ctx, coll):
    true_strings = ['true', 't', 'yes', 'y', '1', '1.0']
    false_strings = ['false', 'f', 'no', 'n', '0', '0.0']

    if len(coll) != 1:
        return []

    val = coll[0]
    var_type = type(val).__name__

    if var_type == "bool":
        return val
    elif var_type == "int" or var_type == "float":
        if val == 1 or val == 1.0:
            return True
        elif val == 0 or val == 0.0:
            return False
    elif var_type == "str":
        lower_case_var = val.lower()
        if lower_case_var in true_strings:
            return True
        if lower_case_var in false_strings:
            return False

    return []


def boolean_singleton(coll):
    d = util.get_data(coll[0])
    if isinstance(d, bool):
        return d
    elif len(coll) == 1:
        return True

def string_singleton(coll):
    d = util.get_data(coll[0])
    if isinstance(d, str):
        return d

singleton_eval_by_type = {
    "Boolean": boolean_singleton,
    "String": string_singleton,
}

def singleton(coll, type):
    if len(coll) > 1:
        raise Exception("Unexpected collection {coll}; expected singleton of type {type}".format(coll=coll, type=type))
    elif len(coll) == 0:
        return []
    to_singleton = singleton_eval_by_type[type]
    if to_singleton:
        val = to_singleton(coll)
        if (val is not None):
            return val
        raise Exception("Expected {type}, but got: {coll}".format(type=type.lower(), coll=coll))
    raise Exception("Not supported type {}".format(type))
