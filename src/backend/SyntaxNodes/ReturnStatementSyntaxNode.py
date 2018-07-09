from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class ReturnStatementSyntaxNode(StatementSyntaxNode):
    def __parseReturn(self, ctx):
        expression = ctx.expression(0).getText()
        return expression

    def __init__(self, ctx, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, nodeType='ReturnStatement', 
            packageName=packageName, className=className, methodSignature=methodSignature, parseSelf=False)
        self.children = []
        self.expression = self.__parseReturn(ctx)
        self.name = self.expression