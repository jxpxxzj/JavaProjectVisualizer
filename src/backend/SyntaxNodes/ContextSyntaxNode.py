from SyntaxNodes.SyntaxNode import SyntaxNode

class ContextSyntaxNode(SyntaxNode):
    def getLineNumber(self, ctx):
        start = ctx.start.line
        stop = ctx.stop.line
        return start, stop

    def parseTypeType(self, ctx):
        variableType = ctx.classOrInterfaceType()
        if variableType is None:
            variableType = ctx.primitiveType()
            return variableType.getText()
        else:
            return variableType.IDENTIFIER()[0].getText()

    
    def __init__(self, ctx, name, nodeType):
        start, stop = self.getLineNumber(ctx)
        super().__init__(name, nodeType, start=start, stop=stop)