from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class AssignStatementSyntaxNode(StatementSyntaxNode):
    def __parseAssignStatement(self, ctx):
        left = ctx.expression(0).getText()
        op = ctx.bop.text
        right = ctx.expression(1).getText()
        return left, op, right
        
    def __init__(self, ctx, name, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, 'AssignStatement', name, packageName, className, methodSignature)
        self.left, self.op, self.right = self.__parseAssignStatement(ctx)
