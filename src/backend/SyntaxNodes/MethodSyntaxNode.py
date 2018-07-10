from antlr4.tree.Tree import TerminalNodeImpl
from SyntaxNodes.ContextSyntaxNode import ContextSyntaxNode
from SyntaxNodes.StatementSyntaxNode import StatementSyntaxNode

class MethodSyntaxNode(ContextSyntaxNode):
    def __parseParameters(self, ctx):
        paramList = []
        if not ctx is None:
            for x in ctx.getChildren():
                if not isinstance(x, TerminalNodeImpl):
                    variableTypeStr = self.parseTypeType(x.typeType())
                    variableName = x.variableDeclaratorId().IDENTIFIER().getText()
            
                    paramTuple = (variableTypeStr, variableName)
                    paramList.append(paramTuple)

        return paramList

    def __init__(self, ctx, nodeType='Method', packageName=None, className=None, parseBody=False):
        super().__init__(ctx, ctx.IDENTIFIER().getText(), nodeType, packageName, className)
        if self.type != 'Constructor':
            self.returnType = ctx.typeTypeOrVoid().getText()
        paramTupleList = self.__parseParameters(ctx.formalParameters().formalParameterList())
        sigList = []
        self.parameters = []
        for x in paramTupleList:
            self.parameters.append(x[0] + ' ' + x[1])
            sigList.append(x[0])
        self.signature = self.name + '(' + ','.join(sigList) + ')'

        if parseBody:
            block = None
            if self.type == 'Constructor':
                block = ctx.constructorBody
            else:
                block = ctx.methodBody().block()
            self.children = StatementSyntaxNode(block, nodeType='MethodBody', name=None, 
                packageName=self.packageName, className=self.className, methodSignature=self.signature).children
        if self.children == None:   
            self.children = []
        
        
