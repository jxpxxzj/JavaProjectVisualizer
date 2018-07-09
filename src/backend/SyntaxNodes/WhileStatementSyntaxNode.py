from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class WhileStatementSyntaxNode(StatementSyntaxNode):
    def __parseWhile(self, ctx):
        condition = ctx.parExpression().expression().getText()
        children = StatementSyntaxNode(ctx.statement(0), nodeType='WhileStatementBlock', 
            packageName=self.packageName, className=self.className, methodSignature=self.methodSignature).children

        return condition, children

    def __init__(self, ctx, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, nodeType='WhileStatement', 
            packageName=packageName, className=className, methodSignature=methodSignature, parseSelf=False)
        self.name, self.children = self.__parseWhile(ctx)
        self.condition = self.name