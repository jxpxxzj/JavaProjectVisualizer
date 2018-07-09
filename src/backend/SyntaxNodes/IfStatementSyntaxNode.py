from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class IfStatementSyntaxNode(StatementSyntaxNode):
    def __parseIf(self, ctx):
        condition = ctx.parExpression().expression().getText()
        trueBranch = StatementSyntaxNode(ctx.statement(0), nodeType='IfTrueBranch', 
            packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)
        falseBranch = None
        if ctx.ELSE() != None: # has else part
            falseBranch = StatementSyntaxNode(ctx.statement(1), nodeType='IfFalseBranch', 
                packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)
        return condition, trueBranch, falseBranch

    def __init__(self, ctx, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, nodeType="IfStatement", 
            packageName=packageName, className=className, methodSignature=methodSignature, parseSelf=False)
            
        self.name, trueBranch, falseBranch = self.__parseIf(ctx)
        self.condition = self.name
        self.children = [trueBranch]
        if falseBranch != None:
            self.children += [falseBranch]