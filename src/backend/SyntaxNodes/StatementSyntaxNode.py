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
            return self.__parseBlock(ctx)

        if hasattr(ctx, 'blockLabel') and ctx.blockLabel != None: # is block
            return self.__parseBlock(ctx.blockLabel)

        if hasattr(ctx, 'statementExpression') and ctx.statementExpression != None: # is expression
            return [self.__parseExpression(ctx.statementExpression)] # returns as a list
        
        if hasattr(ctx, 'RETURN') and ctx.RETURN() != None: # is return      
            from SyntaxNodes.ReturnStatementSyntaxNode import ReturnStatementSyntaxNode
            return [ReturnStatementSyntaxNode(ctx, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)]

        if hasattr(ctx, 'IF') and ctx.IF() != None: # is if statement
            from SyntaxNodes.IfStatementSyntaxNode import IfStatementSyntaxNode
            return [IfStatementSyntaxNode(ctx, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)]

        if hasattr(ctx, 'DO') and ctx.DO() != None: # do..while statement
            from SyntaxNodes.DoWhileStatementSyntaxNode import DoWhileStatementSyntaxNode
            return [DoWhileStatementSyntaxNode(ctx, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)]

        if hasattr(ctx, 'WHILE') and ctx.WHILE() != None: # while statement
            from SyntaxNodes.WhileStatementSyntaxNode import WhileStatementSyntaxNode
            return [WhileStatementSyntaxNode(ctx, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)]

        if hasattr(ctx, 'FOR') and ctx.FOR() != None: # for statement
            from SyntaxNodes.ForStatementSyntaxNode import ForStatementSyntaxNode
            return [ForStatementSyntaxNode(ctx, packageName=self.packageName, className=self.className, methodSignature=self.methodSignature)]

    def __parseBlock(self, ctx):
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
        if parseSelf:
            self.children = self.__parseStatement(ctx)
        
        if self.children == None:
            self.children = []