from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class ForStatementSyntaxNode(StatementSyntaxNode):
    def __parseFor(self, ctx):
        # TODO: parse control condition
        condition = ctx.forControl().getText()
        children = StatementSyntaxNode(ctx.statement(0), nodeType='ForStatementBlock', 
            packageName=self.packageName, className=self.className, methodSignature=self.methodSignature).children

        return condition, children

    def __init__(self, ctx, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, nodeType='ForStatement', 
            packageName=packageName, className=className, methodSignature=methodSignature, parseSelf=False)
        self.condition, self.children = self.__parseFor(ctx)
        self.name = self.condition
