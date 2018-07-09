from SyntaxNodes.ContextSyntaxNode import ContextSyntaxNode

class StatementSyntaxNode(ContextSyntaxNode):
    def __parseMethodCall(self, ctx, nodeType='MethodCall'):
        name = ctx.IDENTIFIER().getText()
        return StatementSyntaxNode(ctx, nodeType, name=name, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)

    def __parseAssign(self, ctx):
        name = ctx.expression(0).getText()
        from SyntaxNodes.AssignStatementSyntaxNode import AssignStatementSyntaxNode
        return AssignStatementSyntaxNode(ctx, name=name, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)

    def __parseExpression(self, ctx, nodeType='MethodCall'):
        if ctx.methodCall() != None:
            return self.__parseMethodCall(ctx.methodCall(), nodeType)

        if len(ctx.expression()) == 2 and ctx.bop.text in ['=', '+=', '-=', '*=', '/=', '&=', '|=', '^=', '>>=', '>>>=', '<<=', '%=']: # assign statement            
            return self.__parseAssign(ctx)


    def __parseStatement(self, ctx):
        statement = None

        if hasattr(ctx, 'blockStatement'):
            statement = self.__parseBlock(ctx)

        if hasattr(ctx, 'blockLabel') and ctx.blockLabel != None: # is block
            statement = self.__parseBlock(ctx.blockLabel)

        if hasattr(ctx, 'statementExpression') and ctx.statementExpression != None: # is expression
            statement = [self.__parseExpression(ctx.statementExpression)] # returns as a list
        
        if hasattr(ctx, 'RETURN') and ctx.RETURN() != None: # is return        
            statement = [self.__parseExpression(ctx.expression(0), 'ReturnStatement')]

        if hasattr(ctx, 'IF') and ctx.IF() != None: # is if statement
            from SyntaxNodes.IfStatementSyntaxNode import IfStatementSyntaxNode
            statement = [IfStatementSyntaxNode(ctx, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)]
        
        return statement

    def __parseBlock(self, ctx):
        # print(ctx.getText())
        statementList = []
        blockStatements = []

        if hasattr(ctx, 'blockStatement'):
            blockStatements = ctx.blockStatement()
        if hasattr(ctx, 'blockLabel') and ctx.blockLabel != None:
            blockStatements = ctx.blockLabel.blockStatement()
              
        for x in blockStatements:
            if x.statement() != None: # is statement
                statement = self.__parseStatement(x.statement())
                if statement != None:
                    statementList += statement
        
        return statementList

    def __init__(self, ctx, nodeType, name=None, packageName=None, className=None, methodSignature=None, parseSelf=True):
        if name == None:
            name = nodeType

        super().__init__(ctx, name=name, nodeType=nodeType, packageName=packageName, className=className)
        self.methodSignature = methodSignature
        # if hasattr(ctx, 'statementExpression') and ctx.statementExpression != None:      
            # statement = 
        if parseSelf:
            self.children = self.__parseStatement(ctx)
        # else:
        #     print(ctx.getText())
        #     self.children = self.__parseStatement(ctx)