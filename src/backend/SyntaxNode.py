class SyntaxNode:
    def __init__(self, name, nodeType=None, start=0, stop=0):
        self.name = name
        self.children = []
        self.type = nodeType
        self.start = start
        self.stop = stop
        self.value = stop - start + 1
    
    def setChildren(self, lst):
        self.children = lst

    def __len__(self):
        return len(self.children)
    
    def __getitem__(self, key):
        if self.__contains__(key):
            return [data for data in self.children if data.name == key][0]
    
    def __contains__(self, key):
        return len([data for data in self.children if data.name == key]) == 1

    def __iter__(self):
        return self.children.__iter__()

    def get(self, key):
        return self.__getitem__(key)

    def append(self, elem):
        self.children.append(elem)

    def getChildrenLineCount(self):
        lineCount = 0
        for x in self.children:
            if (x.type == 'Class') or (x.type == 'Interface'):
                lineCount += x.stop - x.start + 1
            if (x.type == 'Package'):
                lineCount += x.getChildrenLineCount() + 1
        self.value = lineCount
        return lineCount

