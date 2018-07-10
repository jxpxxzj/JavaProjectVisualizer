from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class MethodCallStatementSyntaxNode(StatementSyntaxNode):
    def __parseMethodCall(self, ctx):
        name = ctx.IDENTIFIER().getText()
        value = None
        if ctx.expressionList() != None:
            value = ctx.expressionList().getText()
        return name, value

    def __init__(self, ctx, packageName, className, methodSignature):
        super().__init__(ctx, nodeType='MethodCallStatement',
            packageName=packageName, className=className, methodSignature=methodSignature, parseSelf=False)
        self.name, self.expressionList = self.__parseMethodCall(ctx)