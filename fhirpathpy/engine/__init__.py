import json
import numbers
import fhirpathpy.engine.util as util
from fhirpathpy.engine.nodes import TypeInfo
from fhirpathpy.engine.evaluators import evaluators
from fhirpathpy.engine.invocations import invocations


def check_integer_param(val):
    data = util.get_data(val)
    if int(data) != data:
        raise Exception("Expected integer, got: " + json.dumps(data))
    return data


def check_number_param(val):
    data = util.get_data(val)
    if not isinstance(data, numbers.Number):
        raise Exception("Expected number, got: " + json.dumps(data))
    return data


def check_boolean_param(val):
    data = util.get_data(val)
    if data == True or data == False:
        return data
    raise Exception("Expected boolean, got: " + json.dumps(data))


def check_string_param(val):
    data = util.get_data(val)
    if not isinstance(data, str):
        raise Exception("Expected string, got: " + json.dumps(data))
    return data


def do_eval(ctx, parentData, node):
    node_type = node["type"]

    if node_type in evaluators:
        evaluator = evaluators.get(node_type)
        return evaluator(ctx, parentData, node)

    raise Exception("No " + node_type + " evaluator ")


def doInvoke(ctx, fn_name, data, raw_params):
    if isinstance(fn_name, list) and len(fn_name) == 1:
        fn_name = fn_name[0]

    if type(fn_name) != str or not fn_name in invocations:
        raise Exception("Not implemented: " + str(fn_name))

    invocation = invocations[fn_name]

    if "nullable_input" in invocation and util.is_nullable(data):
        return []

    if not "arity" in invocation:
        if raw_params is None or util.is_empty(raw_params):
            res = invocation["fn"](ctx, util.arraify(data))
            return util.arraify(res)

        raise Exception(fn_name + " expects no params")

    if invocation["fn"].__name__ == "trace_fn" and raw_params is not None:
        raw_params = raw_params[:1]

    paramsNumber = 0
    if isinstance(raw_params, list):
        paramsNumber = len(raw_params)

    if not paramsNumber in invocation["arity"]:
        raise Exception(fn_name + " wrong arity: got " + str(paramsNumber))

    params = []
    argTypes = invocation["arity"][paramsNumber]

    for i in range(0, paramsNumber):
        tp = argTypes[i]
        pr = raw_params[i]
        params.append(make_param(ctx, data, tp, pr))

    params.insert(0, data)
    params.insert(0, ctx)

    if "nullable" in invocation:
        if any(util.is_nullable(x) for x in params):
            return []

    res = invocation["fn"](*params)

    return util.arraify(res)


def type_specifier(ctx, parent_data, node):
    identifiers = node["text"].replace("`", "").split(".")
    namespace = None
    name = None

    if len(identifiers) == 2:
        namespace, name = identifiers
    elif len(identifiers) == 1:
        (name,) = identifiers
    else:
        raise Exception(f"Expected TypeSpecifier node, got {node}")

    return TypeInfo(name=name, namespace=namespace)


param_check_table = {
    "Integer": check_integer_param,
    "Number": check_number_param,
    "Boolean": check_boolean_param,
    "String": check_string_param,
}


def make_param(ctx, parentData, node_type, param):
    if node_type == "Expr":

        def func(data):
            ctx["$this"] = util.arraify(data)
            return do_eval(ctx, ctx["$this"], param)

        return func

    if node_type == "AnyAtRoot":
        ctx["$this"] = ctx["$this"] if "$this" in ctx else ctx["dataRoot"]
        return do_eval(ctx, ctx["$this"], param)

    if node_type == "Identifier":
        if param["type"] == "TermExpression":
            return param["text"]

        raise Exception("Expected identifier node, got " + json.dumps(param))

    if node_type == "TypeSpecifier":
        return type_specifier(ctx, parentData, param)

    ctx["$this"] = parentData
    res = do_eval(ctx, parentData, param)

    if node_type == "Any":
        return res

    if isinstance(node_type, list):
        if len(res) == 0:
            return []
        else:
            node_type = node_type[0]

    if len(res) > 1:
        raise Exception(
            "Unexpected collection" + json.dumps(res) + "; expected singleton of type " + node_type
        )

    if len(res) == 0:
        return []

    if node_type not in param_check_table:
        raise Exception("Implement me for " + node_type)

    check = param_check_table[node_type]

    return check(res[0])


def infix_invoke(ctx, fn_name, data, raw_params):
    if not fn_name in invocations or not "fn" in invocations[fn_name]:
        raise Exception("Not implemented " + fn_name)

    invocation = invocations[fn_name]
    paramsNumber = len(raw_params)

    if paramsNumber != 2:
        raise Exception("Infix invoke should have arity 2")

    argTypes = invocation["arity"][paramsNumber]

    if argTypes is not None:
        params = [ctx]

        for i in range(0, paramsNumber):
            argType = argTypes[i]
            rawParam = raw_params[i]
            params.append(make_param(ctx, data, argType, rawParam))

        if "nullable" in invocation:
            if any(util.is_nullable(x) for x in params):
                return []

        res = invocation["fn"](*params)
        return util.arraify(res)

    print(fn_name + " wrong arity: got " + paramsNumber)
    return []
