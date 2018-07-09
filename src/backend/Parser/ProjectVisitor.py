from antlr4 import *
from Parser.BaseVisitor import BaseVisitor
from SyntaxNodes.MethodSyntaxNode import MethodSyntaxNode
from SyntaxNodes.FieldSyntaxNode import FieldSyntaxNode
from SyntaxNodes.AnnotationTypeElementSyntaxNode import AnnotationTypeElementSyntaxNode

class ProjectVisitor(BaseVisitor):
    def __init__(self, syntaxTree, splitPackage):
        super().__init__(syntaxTree, splitPackage)
    
    def visitMethodDeclaration(self, ctx):
        print('Method: {0}'.format(ctx.IDENTIFIER()))

        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            MethodSyntaxNode(ctx, packageName=self.packageName, className=self.className))
        
        return super().visitMethodDeclaration(ctx)
    
    def visitFieldDeclaration(self, ctx):
        fieldName = ctx.variableDeclarators().variableDeclarator(0).variableDeclaratorId().IDENTIFIER().getText()
        print('Field: {0}'.format(fieldName))
        
        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            FieldSyntaxNode(ctx, packageName=self.packageName, className=self.className))
        
        return super().visitFieldDeclaration(ctx)

    def visitAnnotationTypeElementDeclaration(self, ctx):
        elementName = ctx.annotationTypeElementRest().annotationMethodOrConstantRest().annotationMethodRest().IDENTIFIER().getText()
        print('AnnotationTypeElement: {0}'.format(elementName))
        
        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            AnnotationTypeElementSyntaxNode(ctx, packageName=self.packageName, className=self.className))

        return super().visitAnnotationTypeElementDeclaration(ctx)
    
    def visitInterfaceMethodDeclaration(self, ctx):
        print('InterfaceMethod: {0}'.format(ctx.IDENTIFIER()))
        
        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            MethodSyntaxNode(ctx, nodeType='InterfaceMethod', packageName=self.packageName, className=self.className))
        
        return super().visitInterfaceMethodDeclaration(ctx)

    def visitConstructorDeclaration(self, ctx):
        print('Constructor: {0}'.format(ctx.IDENTIFIER()))

        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            MethodSyntaxNode(ctx, nodeType='Constructor', packageName=self.packageName, className=self.className))

        return super().visitConstructorDeclaration(ctx)
