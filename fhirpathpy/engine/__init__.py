import json
import numbers
import fhirpathpy.engine.util as util
from fhirpathpy.engine.evaluators import evaluators
from fhirpathpy.engine.invocations import invocations


def checkIntegerParam(val):
    data = util.valData(val)
    if int(data) != data:
        raise Exception("Expected integer, got: " + json.dumps(data))
    return data


def checkNumberParam(val):
    data = util.valData(val)
    if not isinstance(data, numbers.Number):
        raise Exception("Expected number, got: " + json.dumps(data))
    return data


def checkBooleanParam(val):
    data = util.valData(val)
    if data == True or data == False:
        return data
    raise Exception("Expected boolean, got: " + json.dumps(data))


def checkStringParam(val):
    data = util.valData(val)
    if not isinstance(data, str):
        raise Exception("Expected string, got: " + json.dumps(data))
    return data


def doEval(ctx, parentData, node):
    nodeType = node["type"]

    if nodeType in evaluators:
        evaluator = evaluators.get(nodeType)
        return evaluator(ctx, parentData, node)

    raise Exception("No " + nodeType + " evaluator ")


def doInvoke(ctx, fnName, data, rawParams):
    if isinstance(fnName, list) and len(fnName) == 1:
        fnName = fnName[0]

    if type(fnName) != str or not fnName in invocations:
        raise Exception("Not implemented: " + str(fnName))

    invocation = invocations[fnName]

    if not "arity" in invocation:
        if rawParams is None or util.isEmpty(rawParams):
            res = invocation["fn"](util.arraify(data))
            return util.arraify(res)

        raise Exception(fnName + " expects no params")

    paramsNumber = 0
    if not util.isEmpty(rawParams):
        paramsNumber = len(rawParams)

    if not paramsNumber in invocation["arity"]:
        print(fnName + " wrong arity: got " + str(paramsNumber))
        return []

    params = []
    argTypes = invocation["arity"][paramsNumber]

    for i in range(0, paramsNumber):
        tp = argTypes[i]
        pr = rawParams[i]
        params.append(makeParam(ctx, data, tp, pr))

    params.insert(0, data)

    if "nullable" in invocation:
        if any(util.isNullable(x) for x in params):
            return []

    res = invocation["fn"](*params)

    return util.arraify(res)


paramCheckTable = {
    "Integer": checkIntegerParam,
    "Number": checkNumberParam,
    "Boolean": checkBooleanParam,
    "String": checkStringParam,
}


def makeParam(ctx, parentData, nodeType, param):
    ctx["currentData"] = parentData

    if nodeType == "Expr":

        def func(data):
            return doEval(ctx, util.arraify(data), param)

        return func

    if nodeType == "AnyAtRoot":
        return doEval(ctx, ctx.dataRoot, param)

    if nodeType == "Identifier":
        if param.type == "TermExpression":
            return param.text

        raise Exception("Expected identifier node, got " + json.dumps(param))

    res = doEval(ctx, parentData, param)

    if nodeType == "Any":
        return res

    if isinstance(nodeType, list):
        if len(res) == 0:
            return []
        else:
            nodeType = nodeType[0]

    if len(res) > 1:
        raise Exception(
            "Unexpected collection"
            + json.dumps(res)
            + "; expected singleton of type "
            + nodeType
        )

    if len(res) == 0:
        return []

    if nodeType not in paramCheckTable:
        raise Exception("Implement me for " + nodeType)

    check = paramCheckTable[nodeType]

    return check(res[0])


def infixInvoke(ctx, fnName, data, rawParams):
    if not fnName in invocations or not "fn" in invocations[fnName]:
        raise Exception("Not implemented " + fnName)

    invocation = invocations[fnName]
    paramsNumber = len(rawParams)

    if paramsNumber != 2:
        raise Exception("Infix invoke should have arity 2")

    argTypes = invocation["arity"][paramsNumber]

    if argTypes is not None:
        params = []

        for i in range(0, paramsNumber):
            argType = argTypes[i]
            rawParam = rawParams[i]
            params.append(makeParam(ctx, data, argType, rawParam))

        if "nullable" in invocation:
            if any(util.isNullable(x) for x in params):
                return []

        res = invocation["fn"](*params)
        return util.arraify(res)

    print(fnName + " wrong arity: got " + paramsNumber)
    return []
