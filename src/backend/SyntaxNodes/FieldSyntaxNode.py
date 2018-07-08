from SyntaxNodes.ContextSyntaxNode import ContextSyntaxNode

class FieldSyntaxNode(ContextSyntaxNode):
    def __init__(self, ctx, packageName=None, className=None):
        fieldName = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        super().__init__(ctx, fieldName, 'Field', packageName, className)
        self.valueType = self.parseTypeType(ctx.typeType())

        