from antlr4 import *
from JavaParserVisitor import JavaParserVisitor
from SyntaxNode import SyntaxNode

class ProjectVisitor(JavaParserVisitor):
    def __init__(self, syntaxTree, splitPackage):
        self.syntaxTree = syntaxTree
        self.packageName = ''
        self.packageTree = None
        self.className = None
        self.splitPackage = splitPackage

    def getLineNumber(self, ctx):
        start = ctx.start.line
        stop = ctx.stop.line
        return start, stop

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
    
    def visitMethodDeclaration(self, ctx):
        start, stop = self.getLineNumber(ctx)
        print('Method: {0} [{1} ~ {2}]'.format(ctx.IDENTIFIER(), start, stop))

        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            SyntaxNode(ctx.IDENTIFIER().getText(), nodeType='Method', start=start, stop=stop))
        
        return super().visitMethodDeclaration(ctx)
    
    def visitInterfaceMethodDeclaration(self, ctx):
        start, stop = self.getLineNumber(ctx)
        print('InterfaceMethod: {0} [{1} ~ {2}]'.format(ctx.IDENTIFIER(), start, stop))
        
        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            SyntaxNode(ctx.IDENTIFIER().getText(), nodeType='InterfaceMethod', start=start, stop=stop))
        
        return super().visitInterfaceMethodDeclaration(ctx)

    def visitConstructorDeclaration(self, ctx):
        start, stop = self.getLineNumber(ctx)
        print('Constructor: {0} [{1} ~ {2}]'.format(ctx.IDENTIFIER(), start, stop))

        self.getPackage(self.syntaxTree, self.packageTree)[self.className].append(
            SyntaxNode(ctx.IDENTIFIER().getText(), nodeType='Constructor', start=start, stop=stop))

        return super().visitConstructorDeclaration(ctx)
    
    def visitAnnotationTypeDeclaration(self, ctx):
        start, stop = self.getLineNumber(ctx)
        self.className = ctx.IDENTIFIER().getText()
        print('Annotation: @{0} [{1} ~ {2}]'.format(self.className, start, stop))

        self.getPackage(self.syntaxTree, self.packageTree).append(
            SyntaxNode('@' + self.className, nodeType='Annotation', start=start, stop=stop))

        return super().visitAnnotationTypeDeclaration(ctx)

    def visitClassDeclaration(self, ctx):
        start, stop = self.getLineNumber(ctx)
        self.className = ctx.IDENTIFIER().getText()
        print('Class: {0} [{1} ~ {2}]'.format(self.className, start, stop))

        self.getPackage(self.syntaxTree, self.packageTree).append(
            SyntaxNode(self.className, nodeType='Class', start=start, stop=stop))

        return super().visitClassDeclaration(ctx)

    def visitInterfaceDeclaration(self, ctx):
        start, stop = self.getLineNumber(ctx)
        self.className = ctx.IDENTIFIER().getText()
        print('Interface: {0} [{1} ~ {2}]'.format(self.className, start, stop))

        self.getPackage(self.syntaxTree, self.packageTree).append(
            SyntaxNode(self.className, nodeType='Interface', start=start, stop=stop))

        return super().visitInterfaceDeclaration(ctx)

    def visitPackageDeclaration(self, ctx):
        self.packageName = ctx.qualifiedName().getText()
        start, stop = self.getLineNumber(ctx)
        print('Package: {0} [{1} ~ {2}]'.format(self.packageName, start, stop))

        if self.splitPackage:
            packageTree = self.parseQualifiedName(ctx.getChild(1)) 
        else:
            packageTree = [self.packageName]
              
        self.packageTree = packageTree       
        self.insertPackage(self.syntaxTree, packageTree)

        return super().visitPackageDeclaration(ctx)