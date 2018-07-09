import os
import os.path

from antlr4 import *
from Parser.JavaLexer import JavaLexer
from Parser.JavaParser import JavaParser
from Parser.ProjectVisitor import ProjectVisitor
from Parser.FileVisitor import FileVisitor
from SyntaxNodes.SyntaxNode import SyntaxNode

def __parseFile(filePath, syntaxTree, splitPackage, visitor, encoding):
    input = FileStream(filePath, encoding)
    lexer = JavaLexer(input)
    stream = CommonTokenStream(lexer)
    parser = JavaParser(stream)
    tree = parser.compilationUnit() 
    vis = visitor(syntaxTree, splitPackage)
    vis.visit(tree)
    syntaxTree.getChildrenLineCount()

def GetFileSyntaxTree(filePath, splitPackage=False, encoding='utf8'):
    syntaxTree = SyntaxNode('File', nodeType='CompilationUnit')
    
    print(filePath)
    __parseFile(filePath, syntaxTree, splitPackage, FileVisitor, encoding)

    return syntaxTree

def GetProjectSyntaxTree(projectPath, splitPackage=False, encoding='utf8'):
    syntaxTree = SyntaxNode('Project', nodeType='CompilationUnit')

    for dirpath, dirnames, filenames in os.walk(projectPath):
        for filename in [f for f in filenames if f.endswith(".java")]:
            files = os.path.join(dirpath, filename)
            print(files)
            __parseFile(files, syntaxTree, splitPackage, ProjectVisitor, encoding)
    
    return syntaxTree

    


    

    

    