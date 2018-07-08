from SyntaxNodes.ContextSyntaxNode import ContextSyntaxNode

class AnnotationTypeElementSyntaxNode(ContextSyntaxNode):
    def __init__(self, ctx, packageName=None, className=None):
        rest = ctx.annotationTypeElementRest()
        #TODO: ignored AnnotationConst
        annoName = rest.annotationMethodOrConstantRest().annotationMethodRest().IDENTIFIER().getText()
        super().__init__(ctx, annoName, 'AnnotationTypeElement', packageName, className)
        self.returnType = self.parseTypeType(rest.typeType())