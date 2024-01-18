# Generated from FHIRPath.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,63,154,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,1,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,38,8,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,5,1,78,8,1,10,1,12,1,81,9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        3,2,90,8,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,100,8,3,1,4,1,4,1,
        4,3,4,105,8,4,1,5,1,5,1,5,1,5,1,5,3,5,112,8,5,1,6,1,6,1,6,3,6,117,
        8,6,1,6,1,6,1,7,1,7,1,7,5,7,124,8,7,10,7,12,7,127,9,7,1,8,1,8,3,
        8,131,8,8,1,9,1,9,1,9,3,9,136,8,9,1,10,1,10,1,11,1,11,1,12,1,12,
        1,13,1,13,1,13,5,13,147,8,13,10,13,12,13,150,9,13,1,14,1,14,1,14,
        0,1,2,15,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,0,12,1,0,4,5,1,
        0,6,9,2,0,4,5,10,10,1,0,12,15,1,0,18,21,1,0,22,23,1,0,25,26,1,0,
        16,17,1,0,32,33,1,0,39,46,1,0,47,54,3,0,16,17,22,23,57,58,171,0,
        30,1,0,0,0,2,37,1,0,0,0,4,89,1,0,0,0,6,99,1,0,0,0,8,101,1,0,0,0,
        10,111,1,0,0,0,12,113,1,0,0,0,14,120,1,0,0,0,16,128,1,0,0,0,18,135,
        1,0,0,0,20,137,1,0,0,0,22,139,1,0,0,0,24,141,1,0,0,0,26,143,1,0,
        0,0,28,151,1,0,0,0,30,31,3,2,1,0,31,32,5,0,0,1,32,1,1,0,0,0,33,34,
        6,1,-1,0,34,38,3,4,2,0,35,36,7,0,0,0,36,38,3,2,1,11,37,33,1,0,0,
        0,37,35,1,0,0,0,38,79,1,0,0,0,39,40,10,10,0,0,40,41,7,1,0,0,41,78,
        3,2,1,11,42,43,10,9,0,0,43,44,7,2,0,0,44,78,3,2,1,10,45,46,10,8,
        0,0,46,47,5,11,0,0,47,78,3,2,1,9,48,49,10,7,0,0,49,50,7,3,0,0,50,
        78,3,2,1,8,51,52,10,5,0,0,52,53,7,4,0,0,53,78,3,2,1,6,54,55,10,4,
        0,0,55,56,7,5,0,0,56,78,3,2,1,5,57,58,10,3,0,0,58,59,5,24,0,0,59,
        78,3,2,1,4,60,61,10,2,0,0,61,62,7,6,0,0,62,78,3,2,1,3,63,64,10,1,
        0,0,64,65,5,27,0,0,65,78,3,2,1,2,66,67,10,13,0,0,67,68,5,1,0,0,68,
        78,3,10,5,0,69,70,10,12,0,0,70,71,5,2,0,0,71,72,3,2,1,0,72,73,5,
        3,0,0,73,78,1,0,0,0,74,75,10,6,0,0,75,76,7,7,0,0,76,78,3,24,12,0,
        77,39,1,0,0,0,77,42,1,0,0,0,77,45,1,0,0,0,77,48,1,0,0,0,77,51,1,
        0,0,0,77,54,1,0,0,0,77,57,1,0,0,0,77,60,1,0,0,0,77,63,1,0,0,0,77,
        66,1,0,0,0,77,69,1,0,0,0,77,74,1,0,0,0,78,81,1,0,0,0,79,77,1,0,0,
        0,79,80,1,0,0,0,80,3,1,0,0,0,81,79,1,0,0,0,82,90,3,10,5,0,83,90,
        3,6,3,0,84,90,3,8,4,0,85,86,5,28,0,0,86,87,3,2,1,0,87,88,5,29,0,
        0,88,90,1,0,0,0,89,82,1,0,0,0,89,83,1,0,0,0,89,84,1,0,0,0,89,85,
        1,0,0,0,90,5,1,0,0,0,91,92,5,30,0,0,92,100,5,31,0,0,93,100,7,8,0,
        0,94,100,5,59,0,0,95,100,5,60,0,0,96,100,5,55,0,0,97,100,5,56,0,
        0,98,100,3,16,8,0,99,91,1,0,0,0,99,93,1,0,0,0,99,94,1,0,0,0,99,95,
        1,0,0,0,99,96,1,0,0,0,99,97,1,0,0,0,99,98,1,0,0,0,100,7,1,0,0,0,
        101,104,5,34,0,0,102,105,3,28,14,0,103,105,5,59,0,0,104,102,1,0,
        0,0,104,103,1,0,0,0,105,9,1,0,0,0,106,112,3,28,14,0,107,112,3,12,
        6,0,108,112,5,35,0,0,109,112,5,36,0,0,110,112,5,37,0,0,111,106,1,
        0,0,0,111,107,1,0,0,0,111,108,1,0,0,0,111,109,1,0,0,0,111,110,1,
        0,0,0,112,11,1,0,0,0,113,114,3,28,14,0,114,116,5,28,0,0,115,117,
        3,14,7,0,116,115,1,0,0,0,116,117,1,0,0,0,117,118,1,0,0,0,118,119,
        5,29,0,0,119,13,1,0,0,0,120,125,3,2,1,0,121,122,5,38,0,0,122,124,
        3,2,1,0,123,121,1,0,0,0,124,127,1,0,0,0,125,123,1,0,0,0,125,126,
        1,0,0,0,126,15,1,0,0,0,127,125,1,0,0,0,128,130,5,60,0,0,129,131,
        3,18,9,0,130,129,1,0,0,0,130,131,1,0,0,0,131,17,1,0,0,0,132,136,
        3,20,10,0,133,136,3,22,11,0,134,136,5,59,0,0,135,132,1,0,0,0,135,
        133,1,0,0,0,135,134,1,0,0,0,136,19,1,0,0,0,137,138,7,9,0,0,138,21,
        1,0,0,0,139,140,7,10,0,0,140,23,1,0,0,0,141,142,3,26,13,0,142,25,
        1,0,0,0,143,148,3,28,14,0,144,145,5,1,0,0,145,147,3,28,14,0,146,
        144,1,0,0,0,147,150,1,0,0,0,148,146,1,0,0,0,148,149,1,0,0,0,149,
        27,1,0,0,0,150,148,1,0,0,0,151,152,7,11,0,0,152,29,1,0,0,0,12,37,
        77,79,89,99,104,111,116,125,130,135,148
    ]

class FHIRPathParser ( Parser ):

    grammarFileName = "FHIRPath.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'.'", "'['", "']'", "'+'", "'-'", "'*'", 
                     "'/'", "'div'", "'mod'", "'&'", "'|'", "'<='", "'<'", 
                     "'>'", "'>='", "'is'", "'as'", "'='", "'~'", "'!='", 
                     "'!~'", "'in'", "'contains'", "'and'", "'or'", "'xor'", 
                     "'implies'", "'('", "')'", "'{'", "'}'", "'true'", 
                     "'false'", "'%'", "'$this'", "'$index'", "'$total'", 
                     "','", "'year'", "'month'", "'week'", "'day'", "'hour'", 
                     "'minute'", "'second'", "'millisecond'", "'years'", 
                     "'months'", "'weeks'", "'days'", "'hours'", "'minutes'", 
                     "'seconds'", "'milliseconds'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "DATETIME", 
                      "TIME", "IDENTIFIER", "DELIMITEDIDENTIFIER", "STRING", 
                      "NUMBER", "WS", "COMMENT", "LINE_COMMENT" ]

    RULE_entireExpression = 0
    RULE_expression = 1
    RULE_term = 2
    RULE_literal = 3
    RULE_externalConstant = 4
    RULE_invocation = 5
    RULE_functn = 6
    RULE_paramList = 7
    RULE_quantity = 8
    RULE_unit = 9
    RULE_dateTimePrecision = 10
    RULE_pluralDateTimePrecision = 11
    RULE_typeSpecifier = 12
    RULE_qualifiedIdentifier = 13
    RULE_identifier = 14

    ruleNames =  [ "entireExpression", "expression", "term", "literal", 
                   "externalConstant", "invocation", "functn", "paramList", 
                   "quantity", "unit", "dateTimePrecision", "pluralDateTimePrecision", 
                   "typeSpecifier", "qualifiedIdentifier", "identifier" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    T__32=33
    T__33=34
    T__34=35
    T__35=36
    T__36=37
    T__37=38
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    T__43=44
    T__44=45
    T__45=46
    T__46=47
    T__47=48
    T__48=49
    T__49=50
    T__50=51
    T__51=52
    T__52=53
    T__53=54
    DATETIME=55
    TIME=56
    IDENTIFIER=57
    DELIMITEDIDENTIFIER=58
    STRING=59
    NUMBER=60
    WS=61
    COMMENT=62
    LINE_COMMENT=63

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class EntireExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,0)


        def EOF(self):
            return self.getToken(FHIRPathParser.EOF, 0)

        def getRuleIndex(self):
            return FHIRPathParser.RULE_entireExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEntireExpression" ):
                listener.enterEntireExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEntireExpression" ):
                listener.exitEntireExpression(self)




    def entireExpression(self):

        localctx = FHIRPathParser.EntireExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_entireExpression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.expression(0)
            self.state = 31
            self.match(FHIRPathParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FHIRPathParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class IndexerExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndexerExpression" ):
                listener.enterIndexerExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndexerExpression" ):
                listener.exitIndexerExpression(self)


    class PolarityExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPolarityExpression" ):
                listener.enterPolarityExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPolarityExpression" ):
                listener.exitPolarityExpression(self)


    class AdditiveExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpression" ):
                listener.enterAdditiveExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpression" ):
                listener.exitAdditiveExpression(self)


    class MultiplicativeExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpression" ):
                listener.enterMultiplicativeExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpression" ):
                listener.exitMultiplicativeExpression(self)


    class UnionExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnionExpression" ):
                listener.enterUnionExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnionExpression" ):
                listener.exitUnionExpression(self)


    class OrExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpression" ):
                listener.enterOrExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpression" ):
                listener.exitOrExpression(self)


    class AndExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpression" ):
                listener.enterAndExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpression" ):
                listener.exitAndExpression(self)


    class MembershipExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMembershipExpression" ):
                listener.enterMembershipExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMembershipExpression" ):
                listener.exitMembershipExpression(self)


    class InequalityExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInequalityExpression" ):
                listener.enterInequalityExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInequalityExpression" ):
                listener.exitInequalityExpression(self)


    class InvocationExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,0)

        def invocation(self):
            return self.getTypedRuleContext(FHIRPathParser.InvocationContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInvocationExpression" ):
                listener.enterInvocationExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInvocationExpression" ):
                listener.exitInvocationExpression(self)


    class EqualityExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqualityExpression" ):
                listener.enterEqualityExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqualityExpression" ):
                listener.exitEqualityExpression(self)


    class ImpliesExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImpliesExpression" ):
                listener.enterImpliesExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImpliesExpression" ):
                listener.exitImpliesExpression(self)


    class TermExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def term(self):
            return self.getTypedRuleContext(FHIRPathParser.TermContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermExpression" ):
                listener.enterTermExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermExpression" ):
                listener.exitTermExpression(self)


    class TypeExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,0)

        def typeSpecifier(self):
            return self.getTypedRuleContext(FHIRPathParser.TypeSpecifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeExpression" ):
                listener.enterTypeExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeExpression" ):
                listener.exitTypeExpression(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = FHIRPathParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16, 17, 22, 23, 28, 30, 32, 33, 34, 35, 36, 37, 55, 56, 57, 58, 59, 60]:
                localctx = FHIRPathParser.TermExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 34
                self.term()
                pass
            elif token in [4, 5]:
                localctx = FHIRPathParser.PolarityExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 35
                _la = self._input.LA(1)
                if not(_la==4 or _la==5):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 36
                self.expression(11)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 79
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 77
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = FHIRPathParser.MultiplicativeExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 39
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 40
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 960) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 41
                        self.expression(11)
                        pass

                    elif la_ == 2:
                        localctx = FHIRPathParser.AdditiveExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 42
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 43
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1072) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 44
                        self.expression(10)
                        pass

                    elif la_ == 3:
                        localctx = FHIRPathParser.UnionExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 45
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 46
                        self.match(FHIRPathParser.T__10)
                        self.state = 47
                        self.expression(9)
                        pass

                    elif la_ == 4:
                        localctx = FHIRPathParser.InequalityExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 48
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 49
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 61440) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 50
                        self.expression(8)
                        pass

                    elif la_ == 5:
                        localctx = FHIRPathParser.EqualityExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 51
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 52
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3932160) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 53
                        self.expression(6)
                        pass

                    elif la_ == 6:
                        localctx = FHIRPathParser.MembershipExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 54
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 55
                        _la = self._input.LA(1)
                        if not(_la==22 or _la==23):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 56
                        self.expression(5)
                        pass

                    elif la_ == 7:
                        localctx = FHIRPathParser.AndExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 57
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 58
                        self.match(FHIRPathParser.T__23)
                        self.state = 59
                        self.expression(4)
                        pass

                    elif la_ == 8:
                        localctx = FHIRPathParser.OrExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 60
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 61
                        _la = self._input.LA(1)
                        if not(_la==25 or _la==26):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 62
                        self.expression(3)
                        pass

                    elif la_ == 9:
                        localctx = FHIRPathParser.ImpliesExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 63
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 64
                        self.match(FHIRPathParser.T__26)
                        self.state = 65
                        self.expression(2)
                        pass

                    elif la_ == 10:
                        localctx = FHIRPathParser.InvocationExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 66
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 67
                        self.match(FHIRPathParser.T__0)
                        self.state = 68
                        self.invocation()
                        pass

                    elif la_ == 11:
                        localctx = FHIRPathParser.IndexerExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 69
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 70
                        self.match(FHIRPathParser.T__1)
                        self.state = 71
                        self.expression(0)
                        self.state = 72
                        self.match(FHIRPathParser.T__2)
                        pass

                    elif la_ == 12:
                        localctx = FHIRPathParser.TypeExpressionContext(self, FHIRPathParser.ExpressionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 74
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 75
                        _la = self._input.LA(1)
                        if not(_la==16 or _la==17):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 76
                        self.typeSpecifier()
                        pass

             
                self.state = 81
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FHIRPathParser.RULE_term

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ExternalConstantTermContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def externalConstant(self):
            return self.getTypedRuleContext(FHIRPathParser.ExternalConstantContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExternalConstantTerm" ):
                listener.enterExternalConstantTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExternalConstantTerm" ):
                listener.exitExternalConstantTerm(self)


    class LiteralTermContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(FHIRPathParser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralTerm" ):
                listener.enterLiteralTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralTerm" ):
                listener.exitLiteralTerm(self)


    class ParenthesizedTermContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenthesizedTerm" ):
                listener.enterParenthesizedTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenthesizedTerm" ):
                listener.exitParenthesizedTerm(self)


    class InvocationTermContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def invocation(self):
            return self.getTypedRuleContext(FHIRPathParser.InvocationContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInvocationTerm" ):
                listener.enterInvocationTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInvocationTerm" ):
                listener.exitInvocationTerm(self)



    def term(self):

        localctx = FHIRPathParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_term)
        try:
            self.state = 89
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16, 17, 22, 23, 35, 36, 37, 57, 58]:
                localctx = FHIRPathParser.InvocationTermContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 82
                self.invocation()
                pass
            elif token in [30, 32, 33, 55, 56, 59, 60]:
                localctx = FHIRPathParser.LiteralTermContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 83
                self.literal()
                pass
            elif token in [34]:
                localctx = FHIRPathParser.ExternalConstantTermContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 84
                self.externalConstant()
                pass
            elif token in [28]:
                localctx = FHIRPathParser.ParenthesizedTermContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 85
                self.match(FHIRPathParser.T__27)
                self.state = 86
                self.expression(0)
                self.state = 87
                self.match(FHIRPathParser.T__28)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FHIRPathParser.RULE_literal

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TimeLiteralContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TIME(self):
            return self.getToken(FHIRPathParser.TIME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimeLiteral" ):
                listener.enterTimeLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimeLiteral" ):
                listener.exitTimeLiteral(self)


    class NullLiteralContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNullLiteral" ):
                listener.enterNullLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNullLiteral" ):
                listener.exitNullLiteral(self)


    class DateTimeLiteralContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DATETIME(self):
            return self.getToken(FHIRPathParser.DATETIME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateTimeLiteral" ):
                listener.enterDateTimeLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateTimeLiteral" ):
                listener.exitDateTimeLiteral(self)


    class StringLiteralContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(FHIRPathParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteral" ):
                listener.enterStringLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteral" ):
                listener.exitStringLiteral(self)


    class BooleanLiteralContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanLiteral" ):
                listener.enterBooleanLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanLiteral" ):
                listener.exitBooleanLiteral(self)


    class NumberLiteralContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(FHIRPathParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberLiteral" ):
                listener.enterNumberLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberLiteral" ):
                listener.exitNumberLiteral(self)


    class QuantityLiteralContext(LiteralContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.LiteralContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def quantity(self):
            return self.getTypedRuleContext(FHIRPathParser.QuantityContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantityLiteral" ):
                listener.enterQuantityLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantityLiteral" ):
                listener.exitQuantityLiteral(self)



    def literal(self):

        localctx = FHIRPathParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.state = 99
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = FHIRPathParser.NullLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 91
                self.match(FHIRPathParser.T__29)
                self.state = 92
                self.match(FHIRPathParser.T__30)
                pass

            elif la_ == 2:
                localctx = FHIRPathParser.BooleanLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 93
                _la = self._input.LA(1)
                if not(_la==32 or _la==33):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 3:
                localctx = FHIRPathParser.StringLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 94
                self.match(FHIRPathParser.STRING)
                pass

            elif la_ == 4:
                localctx = FHIRPathParser.NumberLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 95
                self.match(FHIRPathParser.NUMBER)
                pass

            elif la_ == 5:
                localctx = FHIRPathParser.DateTimeLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 96
                self.match(FHIRPathParser.DATETIME)
                pass

            elif la_ == 6:
                localctx = FHIRPathParser.TimeLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 97
                self.match(FHIRPathParser.TIME)
                pass

            elif la_ == 7:
                localctx = FHIRPathParser.QuantityLiteralContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 98
                self.quantity()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExternalConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(FHIRPathParser.IdentifierContext,0)


        def STRING(self):
            return self.getToken(FHIRPathParser.STRING, 0)

        def getRuleIndex(self):
            return FHIRPathParser.RULE_externalConstant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExternalConstant" ):
                listener.enterExternalConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExternalConstant" ):
                listener.exitExternalConstant(self)




    def externalConstant(self):

        localctx = FHIRPathParser.ExternalConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_externalConstant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self.match(FHIRPathParser.T__33)
            self.state = 104
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [16, 17, 22, 23, 57, 58]:
                self.state = 102
                self.identifier()
                pass
            elif token in [59]:
                self.state = 103
                self.match(FHIRPathParser.STRING)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InvocationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FHIRPathParser.RULE_invocation

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TotalInvocationContext(InvocationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.InvocationContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTotalInvocation" ):
                listener.enterTotalInvocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTotalInvocation" ):
                listener.exitTotalInvocation(self)


    class ThisInvocationContext(InvocationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.InvocationContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterThisInvocation" ):
                listener.enterThisInvocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitThisInvocation" ):
                listener.exitThisInvocation(self)


    class IndexInvocationContext(InvocationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.InvocationContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndexInvocation" ):
                listener.enterIndexInvocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndexInvocation" ):
                listener.exitIndexInvocation(self)


    class FunctionInvocationContext(InvocationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.InvocationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functn(self):
            return self.getTypedRuleContext(FHIRPathParser.FunctnContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionInvocation" ):
                listener.enterFunctionInvocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionInvocation" ):
                listener.exitFunctionInvocation(self)


    class MemberInvocationContext(InvocationContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a FHIRPathParser.InvocationContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def identifier(self):
            return self.getTypedRuleContext(FHIRPathParser.IdentifierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemberInvocation" ):
                listener.enterMemberInvocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemberInvocation" ):
                listener.exitMemberInvocation(self)



    def invocation(self):

        localctx = FHIRPathParser.InvocationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_invocation)
        try:
            self.state = 111
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                localctx = FHIRPathParser.MemberInvocationContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 106
                self.identifier()
                pass

            elif la_ == 2:
                localctx = FHIRPathParser.FunctionInvocationContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 107
                self.functn()
                pass

            elif la_ == 3:
                localctx = FHIRPathParser.ThisInvocationContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 108
                self.match(FHIRPathParser.T__34)
                pass

            elif la_ == 4:
                localctx = FHIRPathParser.IndexInvocationContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 109
                self.match(FHIRPathParser.T__35)
                pass

            elif la_ == 5:
                localctx = FHIRPathParser.TotalInvocationContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 110
                self.match(FHIRPathParser.T__36)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctnContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(FHIRPathParser.IdentifierContext,0)


        def paramList(self):
            return self.getTypedRuleContext(FHIRPathParser.ParamListContext,0)


        def getRuleIndex(self):
            return FHIRPathParser.RULE_functn

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctn" ):
                listener.enterFunctn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctn" ):
                listener.exitFunctn(self)




    def functn(self):

        localctx = FHIRPathParser.FunctnContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_functn)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.identifier()
            self.state = 114
            self.match(FHIRPathParser.T__27)
            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2269814484132626480) != 0):
                self.state = 115
                self.paramList()


            self.state = 118
            self.match(FHIRPathParser.T__28)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.ExpressionContext,i)


        def getRuleIndex(self):
            return FHIRPathParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)




    def paramList(self):

        localctx = FHIRPathParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.expression(0)
            self.state = 125
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==38:
                self.state = 121
                self.match(FHIRPathParser.T__37)
                self.state = 122
                self.expression(0)
                self.state = 127
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantityContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(FHIRPathParser.NUMBER, 0)

        def unit(self):
            return self.getTypedRuleContext(FHIRPathParser.UnitContext,0)


        def getRuleIndex(self):
            return FHIRPathParser.RULE_quantity

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantity" ):
                listener.enterQuantity(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantity" ):
                listener.exitQuantity(self)




    def quantity(self):

        localctx = FHIRPathParser.QuantityContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_quantity)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.match(FHIRPathParser.NUMBER)
            self.state = 130
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 129
                self.unit()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dateTimePrecision(self):
            return self.getTypedRuleContext(FHIRPathParser.DateTimePrecisionContext,0)


        def pluralDateTimePrecision(self):
            return self.getTypedRuleContext(FHIRPathParser.PluralDateTimePrecisionContext,0)


        def STRING(self):
            return self.getToken(FHIRPathParser.STRING, 0)

        def getRuleIndex(self):
            return FHIRPathParser.RULE_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnit" ):
                listener.enterUnit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnit" ):
                listener.exitUnit(self)




    def unit(self):

        localctx = FHIRPathParser.UnitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_unit)
        try:
            self.state = 135
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [39, 40, 41, 42, 43, 44, 45, 46]:
                self.enterOuterAlt(localctx, 1)
                self.state = 132
                self.dateTimePrecision()
                pass
            elif token in [47, 48, 49, 50, 51, 52, 53, 54]:
                self.enterOuterAlt(localctx, 2)
                self.state = 133
                self.pluralDateTimePrecision()
                pass
            elif token in [59]:
                self.enterOuterAlt(localctx, 3)
                self.state = 134
                self.match(FHIRPathParser.STRING)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateTimePrecisionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FHIRPathParser.RULE_dateTimePrecision

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateTimePrecision" ):
                listener.enterDateTimePrecision(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateTimePrecision" ):
                listener.exitDateTimePrecision(self)




    def dateTimePrecision(self):

        localctx = FHIRPathParser.DateTimePrecisionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_dateTimePrecision)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 140187732541440) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PluralDateTimePrecisionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return FHIRPathParser.RULE_pluralDateTimePrecision

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPluralDateTimePrecision" ):
                listener.enterPluralDateTimePrecision(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPluralDateTimePrecision" ):
                listener.exitPluralDateTimePrecision(self)




    def pluralDateTimePrecision(self):

        localctx = FHIRPathParser.PluralDateTimePrecisionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_pluralDateTimePrecision)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 35888059530608640) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeSpecifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qualifiedIdentifier(self):
            return self.getTypedRuleContext(FHIRPathParser.QualifiedIdentifierContext,0)


        def getRuleIndex(self):
            return FHIRPathParser.RULE_typeSpecifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeSpecifier" ):
                listener.enterTypeSpecifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeSpecifier" ):
                listener.exitTypeSpecifier(self)




    def typeSpecifier(self):

        localctx = FHIRPathParser.TypeSpecifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_typeSpecifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.qualifiedIdentifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QualifiedIdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FHIRPathParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(FHIRPathParser.IdentifierContext,i)


        def getRuleIndex(self):
            return FHIRPathParser.RULE_qualifiedIdentifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifiedIdentifier" ):
                listener.enterQualifiedIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifiedIdentifier" ):
                listener.exitQualifiedIdentifier(self)




    def qualifiedIdentifier(self):

        localctx = FHIRPathParser.QualifiedIdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_qualifiedIdentifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.identifier()
            self.state = 148
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 144
                    self.match(FHIRPathParser.T__0)
                    self.state = 145
                    self.identifier() 
                self.state = 150
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(FHIRPathParser.IDENTIFIER, 0)

        def DELIMITEDIDENTIFIER(self):
            return self.getToken(FHIRPathParser.DELIMITEDIDENTIFIER, 0)

        def getRuleIndex(self):
            return FHIRPathParser.RULE_identifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)




    def identifier(self):

        localctx = FHIRPathParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_identifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 432345564240347136) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 1)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 6)
         




