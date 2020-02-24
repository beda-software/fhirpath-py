import sys
from antlr4 import *
from antlr4.tree.Tree import ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import LexerNoViableAltException

from parser.generated.FHIRPathLexer import FHIRPathLexer
from parser.generated.FHIRPathParser import FHIRPathParser
from parser.generated.FHIRPathListener import FHIRPathListener

def recover(self, e):
    raise e


def parse(value): 
    textStream = InputStream(value)

    pathListener = FHIRPathListener()
    errorListener = ErrorListener()
    
    lexer = FHIRPathLexer(textStream)
    lexer.recover = recover
    lexer.removeErrorListeners()
    lexer.addErrorListener(errorListener)

    tokenStream = CommonTokenStream(lexer)

    parser = FHIRPathParser(tokenStream)
    parser.buildParseTrees = True
    parser.removeErrorListeners()
    parser.addErrorListener(errorListener)

    walker = ParseTreeWalker()
    walker.walk(pathListener, parser.expression())

    return { 
      'ast': None,
      'tokens': tokenStream.tokens
    }

