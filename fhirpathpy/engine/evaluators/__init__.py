from functools import reduce

import re
import json
import fhirpathpy.engine as engine
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes


def BooleanLiteral(ctx, parentData, node):
    if node["text"] == "true":
        return [True]
    return [False]


def NumberLiteral(ctx, parentData, node):
    return [float(node["text"])]


def Identifier(ctx, parentData, node):
    return [re.sub(r"(^\"|\"$)", "", node["text"])]


def InvocationTerm(ctx, parentData, node):
    return engine.doEval(ctx, parentData, node["children"][0])


def InvocationExpression(ctx, parentData, node):
    return list(
        reduce(
            lambda accumulator, children: engine.doEval(ctx, accumulator, children),
            node["children"],
            parentData,
        )
    )


def ParamList(ctx, parentData, node):
    # we do not eval param list because sometimes it should be passed as
    # lambda/macro (for example in case of where(...)
    return node


def UnionExpression(ctx, parentData, node):
    return engine.infixInvoke(ctx, "|", parentData, node["children"])


def ThisInvocation(ctx, parentData, node):
    return util.arraify(ctx["currentData"])


def OpExpression(ctx, parentData, node):
    op = node["terminalNodeText"][0]
    return engine.infixInvoke(ctx, op, parentData, node["children"])


def AliasOpExpression(mapFn):
    def func(ctx, parentData, node):
        op = node["terminalNodeText"][0]

        if not op in mapFn:
            raise Exception(
                "Do not know how to alias " + op + " by " + json.dumps(mapFn)
            )

        alias = mapFn[op]
        return engine.infixInvoke(ctx, alias, parentData, node["children"])

    return func


def TermExpression(ctx, parentData, node):
    return engine.doEval(ctx, parentData, node["children"][0])


def NullLiteral():
    return []


def ParenthesizedTerm(ctx, parentData, node):
    return engine.doEval(ctx, parentData, node["children"][0])


def LiteralTerm(ctx, parentData, node):
    term = node["children"][0]

    if term:
        return engine.doEval(ctx, parentData, term)

    return [node["text"]]


def StringLiteral(ctx, parentData, node):
    # Remove the beginning and ending quotes.
    rtn = re.sub(r"^['\"]|['\"]$", "", node["text"])

    rtn = rtn.replace("\\'", "'")
    rtn = rtn.replace('\\"', '"')
    rtn = rtn.replace("\\r", "\r")
    rtn = rtn.replace("\\n", "\n")
    rtn = rtn.replace("\\t", "\t")
    rtn = rtn.replace("\\f", "\f")
    rtn = rtn.replace("\\\\", "\\")

    # TODO
    #  rtn = rtn.replace(/\\(u\d{4}|.)/g, function(match, submatch) {
    #     if (submatch.length > 1)
    #       return String.fromCharCode('0x'+submatch.slice(1));
    #     else
    #       return submatch;

    return [rtn]


def QuantityLiteral(ctx, parentData, node):
    valueNode = node["children"][0]
    value = float(valueNode["terminalNodeText"][0])
    unitNode = valueNode["children"][0]
    unit = unitNode.terminalNodeText[0]
    # Sometimes the unit is in a child node of the child
    if unit is not None and len(unitNode["children"]) > 0:
        unit = unitNode["children"][0]["terminalNodeText"][0]

    return [nodes.FP_Quantity(value, unit)]


def DateTimeLiteral(ctx, parentData, node):
    dateStr = node["text"][:1]
    return [nodes.FP_DateTime(dateStr)]


def TimeLiteral(ctx, parentData, node):
    timeStr = node["text"][:1]
    return [nodes.FP_Time(timeStr)]


def createReduceMemberInvocation(model, key):
    def func(acc, res):
        res = nodes.ResourceNode.makeResNode(res)

        childPath = ""  # res['path'] + '.' + key # TODO

        if model:
            defPath = model["pathsDefinedElsewhere"][childPath]
            if defPath:
                childPath = defPath

        actualTypes = None
        if model and model["choiceTypePaths"]:
            actualTypes = model["choiceTypePaths"][childPath]

        if isinstance(actualTypes, list):
            # Use actualTypes to find the field's value
            for actualType in actualTypes:
                field = key + actualType
                toAdd = res.data[field]
                if toAdd:
                    childPath = actualType
                    break
        else:
            toAdd = res.data[key]

        if util.isSome(toAdd):
            if isinstance(toAdd, list):
                mapped = list(
                    map(lambda x: nodes.ResourceNode.makeResNode(x, childPath), toAdd)
                )
                acc = acc + mapped
            else:
                acc.append(nodes.ResourceNode.makeResNode(toAdd, childPath))
            return acc
        return acc

    return func


def MemberInvocation(ctx, parentData, node):
    key = engine.doEval(ctx, parentData, node["children"][0])[0]
    model = ctx["model"]

    if isinstance(parentData, list):

        if util.isCapitalized(key):
            filtered = list(filter(lambda x: x["resourceType"] == key, parentData))
            mapped = list(
                map(lambda x: nodes.ResourceNode.makeResNode(x, key), filtered)
            )
            return mapped

        return list(reduce(createReduceMemberInvocation(model, key), parentData, []))

    return []


def IndexerExpression(ctx, parentData, node):
    coll_node = node["children"][0]
    idx_node = node["children"][1]

    coll = engine.doEval(ctx, parentData, coll_node)
    idx = engine.doEval(ctx, parentData, idx_node)

    if util.isEmpty(idx):
        return []

    idxNum = int(idx[0])

    if coll is not None and util.isSome(idxNum) and len(coll) > idxNum and idxNum >= 0:
        return [coll[idxNum]]

    return []


def Functn(ctx, parentData, node):
    return list(map(lambda x: engine.doEval(ctx, parentData, x), node["children"]))


def FunctionInvocation(ctx, parentData, node):
    args = engine.doEval(ctx, parentData, node["children"][0])
    fnName = args[0]
    args = args[1:]

    rawParams = None
    if isinstance(args, list) and len(args) > 0 and "children" in args[0]:
        rawParams = args[0]["children"]

    return engine.doInvoke(ctx, fnName, parentData, rawParams)


def PolarityExpression(ctx, parentData, node):
    sign = node["terminalNodeText"][0]
    rtn = engine.doEval(ctx, parentData, node["children"][0])

    if len(rtn) != 1:  # not yet in spec, but per Bryn Rhodes
        raise Exception(
            "Unary " + sign + " can only be applied to an individual number."
        )

    if not util.isNumber(rtn[0]):
        raise Exception("Unary " + sign + " can only be applied to a number.")

    if sign == "-":
        rtn[0] = -rtn[0]

    return rtn


evaluators = {
    "Functn": Functn,
    "ParamList": ParamList,
    "Identifier": Identifier,
    # terms
    "NullLiteral": NullLiteral,
    "LiteralTerm": LiteralTerm,
    "NumberLiteral": NumberLiteral,
    "StringLiteral": StringLiteral,
    "BooleanLiteral": BooleanLiteral,
    "InvocationTerm": InvocationTerm,
    "ParenthesizedTerm": ParenthesizedTerm,
    # Invocations
    "ThisInvocation": ThisInvocation,
    "MemberInvocation": MemberInvocation,
    "FunctionInvocation": FunctionInvocation,
    # expressions
    "PolarityExpression": PolarityExpression,
    "IndexerExpression": IndexerExpression,
    "MembershipExpression": AliasOpExpression({"contains": "containsOp", "in": "inOp"}),
    "TermExpression": TermExpression,
    "UnionExpression": UnionExpression,
    "InvocationExpression": InvocationExpression,
    "InequalityExpression": OpExpression,
    "AdditiveExpression": OpExpression,
    "MultiplicativeExpression": OpExpression,
    "EqualityExpression": OpExpression,
    "OrExpression": OpExpression,
    "ImpliesExpression": OpExpression,
    "AndExpression": OpExpression,
    "XorExpression": OpExpression,
}
