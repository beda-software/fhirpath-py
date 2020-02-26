# Generated from ./FHIRPath.g4 by ANTLR 4.8
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .FHIRPathParser import FHIRPathParser
else:
    from FHIRPathParser import FHIRPathParser

# This class defines a complete listener for a parse tree produced by FHIRPathParser.
class FHIRPathListener(ParseTreeListener):

    # Enter a parse tree produced by FHIRPathParser#indexerExpression.
    def enterIndexerExpression(self, ctx: FHIRPathParser.IndexerExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#indexerExpression.
    def exitIndexerExpression(self, ctx: FHIRPathParser.IndexerExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#polarityExpression.
    def enterPolarityExpression(self, ctx: FHIRPathParser.PolarityExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#polarityExpression.
    def exitPolarityExpression(self, ctx: FHIRPathParser.PolarityExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#additiveExpression.
    def enterAdditiveExpression(self, ctx: FHIRPathParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#additiveExpression.
    def exitAdditiveExpression(self, ctx: FHIRPathParser.AdditiveExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#multiplicativeExpression.
    def enterMultiplicativeExpression(
        self, ctx: FHIRPathParser.MultiplicativeExpressionContext
    ):
        pass

    # Exit a parse tree produced by FHIRPathParser#multiplicativeExpression.
    def exitMultiplicativeExpression(
        self, ctx: FHIRPathParser.MultiplicativeExpressionContext
    ):
        pass

    # Enter a parse tree produced by FHIRPathParser#unionExpression.
    def enterUnionExpression(self, ctx: FHIRPathParser.UnionExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#unionExpression.
    def exitUnionExpression(self, ctx: FHIRPathParser.UnionExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#orExpression.
    def enterOrExpression(self, ctx: FHIRPathParser.OrExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#orExpression.
    def exitOrExpression(self, ctx: FHIRPathParser.OrExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#andExpression.
    def enterAndExpression(self, ctx: FHIRPathParser.AndExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#andExpression.
    def exitAndExpression(self, ctx: FHIRPathParser.AndExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#membershipExpression.
    def enterMembershipExpression(
        self, ctx: FHIRPathParser.MembershipExpressionContext
    ):
        pass

    # Exit a parse tree produced by FHIRPathParser#membershipExpression.
    def exitMembershipExpression(self, ctx: FHIRPathParser.MembershipExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#inequalityExpression.
    def enterInequalityExpression(
        self, ctx: FHIRPathParser.InequalityExpressionContext
    ):
        pass

    # Exit a parse tree produced by FHIRPathParser#inequalityExpression.
    def exitInequalityExpression(self, ctx: FHIRPathParser.InequalityExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#invocationExpression.
    def enterInvocationExpression(
        self, ctx: FHIRPathParser.InvocationExpressionContext
    ):
        pass

    # Exit a parse tree produced by FHIRPathParser#invocationExpression.
    def exitInvocationExpression(self, ctx: FHIRPathParser.InvocationExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#equalityExpression.
    def enterEqualityExpression(self, ctx: FHIRPathParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#equalityExpression.
    def exitEqualityExpression(self, ctx: FHIRPathParser.EqualityExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#impliesExpression.
    def enterImpliesExpression(self, ctx: FHIRPathParser.ImpliesExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#impliesExpression.
    def exitImpliesExpression(self, ctx: FHIRPathParser.ImpliesExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#termExpression.
    def enterTermExpression(self, ctx: FHIRPathParser.TermExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#termExpression.
    def exitTermExpression(self, ctx: FHIRPathParser.TermExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#typeExpression.
    def enterTypeExpression(self, ctx: FHIRPathParser.TypeExpressionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#typeExpression.
    def exitTypeExpression(self, ctx: FHIRPathParser.TypeExpressionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#invocationTerm.
    def enterInvocationTerm(self, ctx: FHIRPathParser.InvocationTermContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#invocationTerm.
    def exitInvocationTerm(self, ctx: FHIRPathParser.InvocationTermContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#literalTerm.
    def enterLiteralTerm(self, ctx: FHIRPathParser.LiteralTermContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#literalTerm.
    def exitLiteralTerm(self, ctx: FHIRPathParser.LiteralTermContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#externalConstantTerm.
    def enterExternalConstantTerm(
        self, ctx: FHIRPathParser.ExternalConstantTermContext
    ):
        pass

    # Exit a parse tree produced by FHIRPathParser#externalConstantTerm.
    def exitExternalConstantTerm(self, ctx: FHIRPathParser.ExternalConstantTermContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#parenthesizedTerm.
    def enterParenthesizedTerm(self, ctx: FHIRPathParser.ParenthesizedTermContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#parenthesizedTerm.
    def exitParenthesizedTerm(self, ctx: FHIRPathParser.ParenthesizedTermContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#nullLiteral.
    def enterNullLiteral(self, ctx: FHIRPathParser.NullLiteralContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#nullLiteral.
    def exitNullLiteral(self, ctx: FHIRPathParser.NullLiteralContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx: FHIRPathParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx: FHIRPathParser.BooleanLiteralContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#stringLiteral.
    def enterStringLiteral(self, ctx: FHIRPathParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#stringLiteral.
    def exitStringLiteral(self, ctx: FHIRPathParser.StringLiteralContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#numberLiteral.
    def enterNumberLiteral(self, ctx: FHIRPathParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#numberLiteral.
    def exitNumberLiteral(self, ctx: FHIRPathParser.NumberLiteralContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#dateTimeLiteral.
    def enterDateTimeLiteral(self, ctx: FHIRPathParser.DateTimeLiteralContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#dateTimeLiteral.
    def exitDateTimeLiteral(self, ctx: FHIRPathParser.DateTimeLiteralContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#timeLiteral.
    def enterTimeLiteral(self, ctx: FHIRPathParser.TimeLiteralContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#timeLiteral.
    def exitTimeLiteral(self, ctx: FHIRPathParser.TimeLiteralContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#quantityLiteral.
    def enterQuantityLiteral(self, ctx: FHIRPathParser.QuantityLiteralContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#quantityLiteral.
    def exitQuantityLiteral(self, ctx: FHIRPathParser.QuantityLiteralContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#externalConstant.
    def enterExternalConstant(self, ctx: FHIRPathParser.ExternalConstantContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#externalConstant.
    def exitExternalConstant(self, ctx: FHIRPathParser.ExternalConstantContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#memberInvocation.
    def enterMemberInvocation(self, ctx: FHIRPathParser.MemberInvocationContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#memberInvocation.
    def exitMemberInvocation(self, ctx: FHIRPathParser.MemberInvocationContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#functionInvocation.
    def enterFunctionInvocation(self, ctx: FHIRPathParser.FunctionInvocationContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#functionInvocation.
    def exitFunctionInvocation(self, ctx: FHIRPathParser.FunctionInvocationContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#thisInvocation.
    def enterThisInvocation(self, ctx: FHIRPathParser.ThisInvocationContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#thisInvocation.
    def exitThisInvocation(self, ctx: FHIRPathParser.ThisInvocationContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#functn.
    def enterFunctn(self, ctx: FHIRPathParser.FunctnContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#functn.
    def exitFunctn(self, ctx: FHIRPathParser.FunctnContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#paramList.
    def enterParamList(self, ctx: FHIRPathParser.ParamListContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#paramList.
    def exitParamList(self, ctx: FHIRPathParser.ParamListContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#quantity.
    def enterQuantity(self, ctx: FHIRPathParser.QuantityContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#quantity.
    def exitQuantity(self, ctx: FHIRPathParser.QuantityContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#unit.
    def enterUnit(self, ctx: FHIRPathParser.UnitContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#unit.
    def exitUnit(self, ctx: FHIRPathParser.UnitContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#dateTimePrecision.
    def enterDateTimePrecision(self, ctx: FHIRPathParser.DateTimePrecisionContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#dateTimePrecision.
    def exitDateTimePrecision(self, ctx: FHIRPathParser.DateTimePrecisionContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#pluralDateTimePrecision.
    def enterPluralDateTimePrecision(
        self, ctx: FHIRPathParser.PluralDateTimePrecisionContext
    ):
        pass

    # Exit a parse tree produced by FHIRPathParser#pluralDateTimePrecision.
    def exitPluralDateTimePrecision(
        self, ctx: FHIRPathParser.PluralDateTimePrecisionContext
    ):
        pass

    # Enter a parse tree produced by FHIRPathParser#typeSpecifier.
    def enterTypeSpecifier(self, ctx: FHIRPathParser.TypeSpecifierContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#typeSpecifier.
    def exitTypeSpecifier(self, ctx: FHIRPathParser.TypeSpecifierContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#qualifiedIdentifier.
    def enterQualifiedIdentifier(self, ctx: FHIRPathParser.QualifiedIdentifierContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#qualifiedIdentifier.
    def exitQualifiedIdentifier(self, ctx: FHIRPathParser.QualifiedIdentifierContext):
        pass

    # Enter a parse tree produced by FHIRPathParser#identifier.
    def enterIdentifier(self, ctx: FHIRPathParser.IdentifierContext):
        pass

    # Exit a parse tree produced by FHIRPathParser#identifier.
    def exitIdentifier(self, ctx: FHIRPathParser.IdentifierContext):
        pass


del FHIRPathParser
