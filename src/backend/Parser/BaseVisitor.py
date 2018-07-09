from antlr4 import *
from Parser.JavaParserVisitor import JavaParserVisitor
from SyntaxNodes.SyntaxNode import SyntaxNode
from SyntaxNodes.ContextSyntaxNode import ContextSyntaxNode

class BaseVisitor(JavaParserVisitor):
    def __init__(self, syntaxTree=None, splitPackage=False):
        self.syntaxTree = syntaxTree
        self.packageName = ''
        self.packageTree = None
        self.className = None
        self.splitPackage = splitPackage

    def parseQualifiedName(self, ctx):
        qualifiedNames = ctx.getChildren()
        identifierList = []
        for x in qualifiedNames:
            text = x.getText()
            if text != '.':
                identifierList.append(text)
        return identifierList

    def insertPackage(self, subTree, packageTree):
        if len(packageTree) == 0:
            return
        else:
            if not packageTree[0] in subTree:
                subTree.append(SyntaxNode(packageTree[0], nodeType='Package'))
            self.insertPackage(subTree[packageTree[0]], packageTree[1:])
    
    def getPackage(self, subTree, packageTree):
        if len(packageTree) == 1:
            return subTree[packageTree[0]]
        else:
            if packageTree[0] in subTree:
                return self.getPackage(subTree[packageTree[0]], packageTree[1:])
            else:
                return None    
    
    def visitAnnotationTypeDeclaration(self, ctx):
        self.className = ctx.IDENTIFIER().getText()
        print('Annotation: @{0}'.format(self.className))

        self.getPackage(self.syntaxTree, self.packageTree).append(
            ContextSyntaxNode(ctx, self.className, nodeType='Annotation', packageName=self.packageName))

        return super().visitAnnotationTypeDeclaration(ctx)
        
    def visitClassDeclaration(self, ctx):
        self.className = ctx.IDENTIFIER().getText()
        print('Class: {0}'.format(self.className))

        self.getPackage(self.syntaxTree, self.packageTree).append(
            ContextSyntaxNode(ctx, self.className, nodeType='Class', packageName=self.packageName))

        return super().visitClassDeclaration(ctx)

    def visitInterfaceDeclaration(self, ctx):
        self.className = ctx.IDENTIFIER().getText()
        print('Interface: {0}]'.format(self.className))

        self.getPackage(self.syntaxTree, self.packageTree).append(
            ContextSyntaxNode(ctx, self.className, nodeType='Interface', packageName=self.packageName))

        return super().visitInterfaceDeclaration(ctx)

    def visitPackageDeclaration(self, ctx):
        self.packageName = ctx.qualifiedName().getText()
        print('Package: {0}'.format(self.packageName))

        if self.splitPackage:
            packageTree = self.parseQualifiedName(ctx.getChild(1)) 
        else:
            packageTree = [self.packageName]
              
        self.packageTree = packageTree       
        self.insertPackage(self.syntaxTree, packageTree)

        return super().visitPackageDeclaration(ctx)
