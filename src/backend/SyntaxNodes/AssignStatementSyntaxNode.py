from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class AssignStatementSyntaxNode(StatementSyntaxNode):
    def __parseAssignStatement(self, ctx):
        left = ctx.expression(0).getText()
        op = ctx.bop.text
        right = ctx.expression(1).getText()
        return left, op, right
        
    def __init__(self, ctx, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, nodeType='AssignStatement', 
            packageName=packageName, className=className, methodSignature=methodSignature)
        self.left, self.op, self.right = self.__parseAssignStatement(ctx)
        self.name = self.left
