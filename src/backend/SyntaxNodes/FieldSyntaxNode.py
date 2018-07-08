from SyntaxNodes.ContextSyntaxNode import ContextSyntaxNode

class FieldSyntaxNode(ContextSyntaxNode):
    def __init__(self, ctx):
        fieldName = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        super().__init__(ctx, fieldName, 'Field')
        self.valueType = self.parseTypeType(ctx.typeType())

        