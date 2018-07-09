from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class DoWhileStatementSyntaxNode(StatementSyntaxNode):
    def __parseDoWhile(self, ctx):
        condition = ctx.parExpression().expression().getText()
        children = StatementSyntaxNode(ctx.statement(0), nodeType='DoWhileStatementBlock', 
            packageName=self.packageName, className=self.className, methodSignature=self.methodSignature).children

        return condition, children

    def __init__(self, ctx, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, nodeType='DoWhileStatement', 
            packageName=packageName, className=className, methodSignature=methodSignature, parseSelf=False)
        
        self.condition, self.children = self.__parseDoWhile(ctx)
        self.name = self.condition