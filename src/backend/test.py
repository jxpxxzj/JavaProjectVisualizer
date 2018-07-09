import sys
import os.path

import json
from Parser.SyntaxTree import GetProjectSyntaxTree, GetFileSyntaxTree
from Utils.NodeEncoder import NodeEncoder
from Utils.ZipUtils import UnzipFile
from FileNodes.FileTree import GetFileTree

from Server.App import CreateApp

def srcTree(argv):
    sourceTree = GetProjectSyntaxTree(argv[1])
    strs = json.dumps(sourceTree, sort_keys=True, cls=NodeEncoder)
    with open('srcTree.json', 'w') as f:
       f.write(strs)
    # print(strs)

def fileSrcTree(argv):
    sourceTree = GetFileSyntaxTree(argv[1])
    strs = json.dumps(sourceTree, sort_keys=True, cls=NodeEncoder)
    with open('fileSrcTree.json', 'w') as f:
       f.write(strs)

def fileTree(argv):
    fileTree = GetFileTree(argv[1])
    strs = json.dumps(fileTree, sort_keys=True, cls=NodeEncoder)
    # with open('fileTree.json', 'w') as f:
    #    f.write(strs)
    print(strs)

def testUnzip(argv):
    UnzipFile(argv[1])

def testFlask(argv):
    app = CreateApp()
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    sys.path.append(os.path.dirname(sys.path[0]))
    # srcTree(sys.argv)
    fileSrcTree(sys.argv)
    # testFlask(sys.argv)
    # fileTree(sys.argv)
    # testUnzip(sys.argv)
