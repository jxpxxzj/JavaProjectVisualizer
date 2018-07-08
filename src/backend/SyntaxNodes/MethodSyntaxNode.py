from antlr4.tree.Tree import TerminalNodeImpl
from SyntaxNodes.ContextSyntaxNode import ContextSyntaxNode

class MethodSyntaxNode(ContextSyntaxNode):
    def parseSignature(self, ctx):
        sigList = []
        if not ctx is None:
            for x in ctx.getChildren():
                if not isinstance(x, TerminalNodeImpl):
                    variableTypeStr = self.parseTypeType(x.typeType())
                    variableName = x.variableDeclaratorId().IDENTIFIER().getText()
            
                    sigStr = variableTypeStr + ' ' + variableName
                    sigList.append(sigStr)

            return sigList
        return ''

    def __init__(self, ctx, nodeType='Method', packageName=None, className=None):
        super().__init__(ctx, ctx.IDENTIFIER().getText(), nodeType, packageName, className)
        if self.type != 'Constructor':
            self.returnType = ctx.typeTypeOrVoid().getText()
        self.signature = self.parseSignature(ctx.formalParameters().formalParameterList())
