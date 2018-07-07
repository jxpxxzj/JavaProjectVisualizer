import sys
import os.path

import json
from SyntaxTree import GetProjectSyntaxTree
from NodeEncoder import NodeEncoder
from ZipUtils import UnzipFile
from FileTree import GetFileTree

def srcTree(argv):
    sourceTree = GetProjectSyntaxTree(argv[1])
    strs = json.dumps(sourceTree, sort_keys=True, cls=NodeEncoder, indent=4)
    with open('srcTree.json', 'w') as f:
        f.write(strs)
    print(strs)

def fileTree(argv):
    fileTree = GetFileTree(argv[1])
    strs = json.dumps(tree, sort_keys=True, cls=NodeEncoder)
    with open('srcTree.json', 'w') as f:
        f.write(strs)
    print(strs)

def testUnzip(argv):
    UnzipFile(argv[1])

if __name__ == '__main__':
    sys.path.append(os.path.dirname(sys.path[0]))
    srcTree(sys.argv)
    # fileTree(sys.argv)
    # testUnzip(sys.argv)
