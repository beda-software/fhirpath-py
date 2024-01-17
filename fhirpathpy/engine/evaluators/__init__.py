from decimal import Decimal
from functools import reduce

import re
import json
import fhirpathpy.engine as engine
import fhirpathpy.engine.util as util
import fhirpathpy.engine.nodes as nodes


def boolean_literal(ctx, parentData, node):
    if node["text"] == "true":
        return [True]
    return [False]


def number_literal(ctx, parentData, node):
    decimal_number = Decimal(node["text"])
    int_number = int(decimal_number)

    return [int_number] if decimal_number == int_number else [decimal_number]


def identifier(ctx, parentData, node):
    return [re.sub(r"(^\"|\"$)", "", node["text"])]


def invocation_term(ctx, parentData, node):
    return engine.do_eval(ctx, parentData, node["children"][0])


def invocation_expression(ctx, parentData, node):
    return list(
        reduce(
            lambda accumulator, children: engine.do_eval(ctx, accumulator, children),
            node["children"],
            parentData,
        )
    )


def param_list(ctx, parentData, node):
    # we do not eval param list because sometimes it should be passed as
    # lambda/macro (for example in case of where(...)
    return node


def union_expression(ctx, parentData, node):
    return engine.infix_invoke(ctx, "|", parentData, node["children"])


def index_invocation(ctx, parentData, node):
    return util.arraify(ctx["$index"])


def this_invocation(ctx, parentData, node):
    return util.arraify(ctx["$this"])


def total_invocation(ctx, parentData, node):
    return util.arraify(ctx["$total"])


def op_expression(ctx, parentData, node):
    op = node["terminalNodeText"][0]
    return engine.infix_invoke(ctx, op, parentData, node["children"])


def alias_op_expression(mapFn):
    def func(ctx, parentData, node):
        op = node["terminalNodeText"][0]

        if not op in mapFn:
            raise Exception("Do not know how to alias " + op + " by " + json.dumps(mapFn))

        alias = mapFn[op]
        return engine.infix_invoke(ctx, alias, parentData, node["children"])

    return func


def term_expression(ctx, parentData, node):
    return engine.do_eval(ctx, parentData, node["children"][0])


def null_literal(ctx, parentData, node):
    return []


def parenthesized_term(ctx, parentData, node):
    return engine.do_eval(ctx, parentData, node["children"][0])


def literal_term(ctx, parentData, node):
    term = node["children"][0]

    if term:
        return engine.do_eval(ctx, parentData, term)

    return [node["text"]]


def external_constant_term(ctx, parent_data, node):
    ext_constant = node["children"][0]
    ext_identifier = ext_constant["children"][0]
    varName = identifier(ctx, parent_data, ext_identifier)[0].replace("`", "")

    if not varName in ctx["vars"]:
        return []

    value = ctx["vars"][varName]

    # For convenience, we all variable values to be passed in without their array
    # wrapper.  However, when evaluating, we need to put the array back in.

    if value is None:
        return []

    if not isinstance(value, list):
        return [value]

    return value


def match(m):
    code = m.group(1)
    return chr(int(code[1:], 16))


def string_literal(ctx, parentData, node):
    # Remove the beginning and ending quotes.
    rtn = re.sub(r"^['\"]|['\"]$", "", node["text"])

    rtn = rtn.replace("\\'", "'")
    rtn = rtn.replace("\\`", "`")
    rtn = rtn.replace('\\"', '"')
    rtn = rtn.replace("\\r", "\r")
    rtn = rtn.replace("\\n", "\n")
    rtn = rtn.replace("\\t", "\t")
    rtn = rtn.replace("\\f", "\f")
    rtn = rtn.replace("\\\\", "\\")
    rtn = re.sub(r"\\(u\d{4})", match, rtn)

    return [rtn]


def quantity_literal(ctx, parentData, node):
    valueNode = node["children"][0]
    value = Decimal(valueNode["terminalNodeText"][0])
    unitNode = valueNode["children"][0]
    if len(unitNode["terminalNodeText"]) > 0:
        unit = unitNode["terminalNodeText"][0]
    # Sometimes the unit is in a child node of the child
    elif "children" in unitNode and len(unitNode["children"]) > 0:
        unit = unitNode["children"][0]["terminalNodeText"][0]
    else:
        unit = None

    return [nodes.FP_Quantity(value, unit)]


def date_time_literal(ctx, parentData, node):
    dateStr = node["text"][1:]
    return [nodes.FP_DateTime(dateStr)]


def time_literal(ctx, parentData, node):
    timeStr = node["text"][2:]
    return [nodes.FP_Time(timeStr)]


def create_reduce_member_invocation(model, key):
    def func(acc, res):
        res = nodes.ResourceNode.create_node(res)
        childPath = f"{res.path}.{key}" if res.path else f"_.{key}"

        actualTypes = None
        toAdd = None
        toAdd_ = None

        if isinstance(model, dict):
            childPath = model["pathsDefinedElsewhere"].get(childPath, childPath)
            actualTypes = model["choiceTypePaths"].get(childPath)

        if isinstance(res.data, nodes.FP_Quantity):
            toAdd = res.data.value

        if actualTypes and isinstance(res.data, dict):
            # Use actualTypes to find the field's value
            for actualType in actualTypes:
                field = f"{key}{actualType}"
                toAdd = res.data.get(field)
                toAdd_ = res.data.get(f"_{field}")
                if toAdd is not None or toAdd_ is not None:
                    childPath += actualType
                    break
        elif isinstance(res.data, dict):
            toAdd = res.data.get(key)
            toAdd_ = res.data.get(f"_{key}")
            if key == "extension":
                childPath = "Extension"
        else:
            if key == "length":
                toAdd = len(res.data)

        childPath = (
            model["path2Type"].get(childPath, childPath)
            if isinstance(model, dict) and "path2Type" in model
            else childPath
        )

        if util.is_some(toAdd):
            if isinstance(toAdd, list):
                mapped = [nodes.ResourceNode.create_node(x, childPath) for x in toAdd]
                acc = acc + mapped
            else:
                acc.append(nodes.ResourceNode.create_node(toAdd, childPath))
        if util.is_some(toAdd_):
            if isinstance(toAdd_, list):
                mapped = [nodes.ResourceNode.create_node(x, childPath) for x in toAdd_]
                acc = acc + mapped
            else:
                acc.append(nodes.ResourceNode.create_node(toAdd_, childPath))
        return acc

    return func


def member_invocation(ctx, parentData, node):
    key = engine.do_eval(ctx, parentData, node["children"][0])[0].replace("`", "")
    model = ctx["model"]

    if isinstance(parentData, list):
        if util.is_capitalized(key):
            try:
                filtered = [x for x in parentData if x["resourceType"] == key]
                mapped = [nodes.ResourceNode.create_node(x, key) for x in filtered]

                return mapped
            except TypeError:
                pass

        return list(reduce(create_reduce_member_invocation(model, key), parentData, []))

    return []


def indexer_expression(ctx, parentData, node):
    coll_node = node["children"][0]
    idx_node = node["children"][1]

    coll = engine.do_eval(ctx, parentData, coll_node)
    idx = engine.do_eval(ctx, parentData, idx_node)

    if util.is_empty(idx):
        return []

    idxNum = int(idx[0])

    if coll is not None and util.is_some(idxNum) and len(coll) > idxNum and idxNum >= 0:
        return [coll[idxNum]]

    return []


def functn(ctx, parentData, node):
    return [engine.do_eval(ctx, parentData, x) for x in node["children"]]


def function_invocation(ctx, parentData, node):
    args = engine.do_eval(ctx, parentData, node["children"][0])
    fn_name = args[0]
    args = args[1:]

    raw_params = None
    if isinstance(args, list) and len(args) > 0 and "children" in args[0]:
        raw_params = args[0]["children"]

    return engine.doInvoke(ctx, fn_name, parentData, raw_params)


def polarity_expression(ctx, parentData, node):
    sign = node["terminalNodeText"][0]
    rtn = engine.do_eval(ctx, parentData, node["children"][0])

    if len(rtn) != 1:  # not yet in spec, but per Bryn Rhodes
        raise Exception("Unary " + sign + " can only be applied to an individual number.")

    if not util.is_number(rtn[0]):
        raise Exception("Unary " + sign + " can only be applied to a number.")

    if sign == "-":
        rtn[0] = -rtn[0]

    return rtn


evaluators = {
    "Functn": functn,
    "ParamList": param_list,
    "Identifier": identifier,
    # terms
    "NullLiteral": null_literal,
    "LiteralTerm": literal_term,
    "NumberLiteral": number_literal,
    "StringLiteral": string_literal,
    "BooleanLiteral": boolean_literal,
    "QuantityLiteral": quantity_literal,
    "DateTimeLiteral": date_time_literal,
    "TimeLiteral": time_literal,
    "InvocationTerm": invocation_term,
    "ParenthesizedTerm": parenthesized_term,
    "ExternalConstantTerm": external_constant_term,
    # Invocations
    "ThisInvocation": this_invocation,
    "MemberInvocation": member_invocation,
    "FunctionInvocation": function_invocation,
    "IndexInvocation": index_invocation,
    "TotalInvocation": total_invocation,
    # expressions
    "PolarityExpression": polarity_expression,
    "IndexerExpression": indexer_expression,
    "MembershipExpression": alias_op_expression({"contains": "containsOp", "in": "inOp"}),
    "TermExpression": term_expression,
    "UnionExpression": union_expression,
    "InvocationExpression": invocation_expression,
    "InequalityExpression": op_expression,
    "AdditiveExpression": op_expression,
    "MultiplicativeExpression": op_expression,
    "TypeExpression": alias_op_expression({"is": "isOp", "as": "asOp"}),
    "EqualityExpression": op_expression,
    "OrExpression": op_expression,
    "ImpliesExpression": op_expression,
    "AndExpression": op_expression,
    "XorExpression": op_expression,
}
