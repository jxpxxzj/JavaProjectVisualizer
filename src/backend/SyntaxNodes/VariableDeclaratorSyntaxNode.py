from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class VariableDeclaratorSyntaxNode(StatementSyntaxNode):
    def __parseVariableDeclarator(self, ctx):
        name = ctx.variableDeclaratorId().getText()
        value = ''
        if ctx.variableInitializer() != None:
            value = ctx.variableInitializer().getText()
        return name, value
        
    def __init__(self, ctx, valueType, packageName=None, className=None, methodSignature=None):
        super().__init__(ctx, nodeType='VariableDeclarator', 
            packageName=packageName, className=className, methodSignature=methodSignature, parseSelf=False)
        self.left, self.right = self.__parseVariableDeclarator(ctx)
        self.name = self.left
        self.valueType = valueType
