from json import JSONEncoder

class NodeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  