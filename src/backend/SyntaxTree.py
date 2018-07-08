import os
import os.path

from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from ProjectVisitor import ProjectVisitor
from SyntaxNodes.SyntaxNode import SyntaxNode

def __parseFile(filePath, syntaxTree, splitPackage, encoding):
    input = FileStream(filePath, encoding)
    lexer = JavaLexer(input)
    stream = CommonTokenStream(lexer)
    parser = JavaParser(stream)
    tree = parser.compilationUnit() 
    visitor = ProjectVisitor(syntaxTree, splitPackage)
    visitor.visit(tree)

def GetFileSyntaxTree(filePath, splitPackage=False, encoding='utf8'):
    syntaxTree = SyntaxNode('File', nodeType='CompilationUnit')
    
    print(filePath)
    __parseFile(filePath, syntaxTree, splitPackage, encoding)

    syntaxTree.getChildrenLineCount()

    return syntaxTree

def GetProjectSyntaxTree(projectPath, splitPackage=False, encoding='utf8'):
    syntaxTree = SyntaxNode('Project', nodeType='CompilationUnit')

    for dirpath, dirnames, filenames in os.walk(projectPath):
        for filename in [f for f in filenames if f.endswith(".java")]:
            files = os.path.join(dirpath, filename)
            print(files)
            __parseFile(files, syntaxTree, splitPackage, encoding)

    syntaxTree.getChildrenLineCount()

    return syntaxTree

    


    

    

    