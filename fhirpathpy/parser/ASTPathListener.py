from antlr4.tree.Tree import TerminalNodeImpl
from fhirpathpy.parser.generated.FHIRPathListener import FHIRPathListener


def has_node_type_text(node_type):
    # In general we need mostly terminal nodes (e.g. Identifier and any Literal)
    # But the code also uses TypeSpecifier, InvocationExpression and TermExpression
    return node_type.endswith("Literal") or node_type in [
        "LiteralTerm",
        "Identifier",
        "TypeSpecifier",
        "InvocationExpression",
        "TermExpression",
    ]


class ASTPathListener(FHIRPathListener):
    def __init__(self):
        self.parentStack = [{}]

    def pushNode(self, nodeType, ctx):
        parentNode = self.parentStack[-1]
        node = {"type": nodeType, "terminalNodeText": []}
        if has_node_type_text(nodeType):
            node["text"] = ctx.getText()
        for child in ctx.children:
            if isinstance(child, TerminalNodeImpl):
                node["terminalNodeText"].append(child.getText())

        if "children" not in parentNode:
            parentNode["children"] = []

        parentNode["children"].append(node)

        self.parentStack.append(node)

    def popNode(self):
        if len(self.parentStack) > 0:
            self.parentStack.pop()

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)

        if name in FHIRPathListener.__dict__ and callable(attr):

            def newfunc(*args, **kwargs):
                if name.startswith("enter"):
                    self.pushNode(name[5:], args[0])

                if name.startswith("exit"):
                    self.popNode()

                return attr(*args, **kwargs)

            return newfunc
        return attr
