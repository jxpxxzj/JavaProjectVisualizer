from antlr4 import *
from Parser.BaseVisitor import BaseVisitor

from SyntaxNodes.MethodSyntaxNode import MethodSyntaxNode


class FileVisitor(BaseVisitor):
    def __init__(self, syntaxTree, splitPackage=False):
        super().__init__(syntaxTree, splitPackage)

    def visitMethodDeclaration(self, ctx):
        print('Method: {0}'.format(ctx.IDENTIFIER()))

        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            MethodSyntaxNode(ctx, packageName=self.packageName, className=self.className, parseBody=True))
        
        return super().visitMethodDeclaration(ctx)

