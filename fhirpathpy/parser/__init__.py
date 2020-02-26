import sys
from antlr4 import *
from antlr4.tree.Tree import ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import LexerNoViableAltException
from fhirpathpy.parser.generated.FHIRPathLexer import FHIRPathLexer
from fhirpathpy.parser.generated.FHIRPathParser import FHIRPathParser
from fhirpathpy.parser.ASTPathListener import ASTPathListener


def recover(e):
    raise e


def parse(value):
    textStream = InputStream(value)

    astPathListener = ASTPathListener()
    errorListener = ErrorListener()

    lexer = FHIRPathLexer(textStream)
    lexer.recover = recover
    lexer.removeErrorListeners()
    lexer.addErrorListener(errorListener)

    parser = FHIRPathParser(CommonTokenStream(lexer))
    parser.buildParseTrees = True
    parser.removeErrorListeners()
    parser.addErrorListener(errorListener)

    walker = ParseTreeWalker()
    walker.walk(astPathListener, parser.expression())

    return astPathListener.parentStack[0]
