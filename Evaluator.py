from Nodes import Node
from functools import reduce


class Evaluator(object):
    def __init__(self) -> None:
        self.globalmemory = {}

    def __str__(self) -> str:
        return 'Evaluator'

    def __repr__(self) -> str:
        return self.__str__()

    def evaluate(self, nodes: Node, pos: int = 0) -> None:
        node = nodes[pos]
        node(self.globalmemory)
        if pos+1 >= len(nodes):
            memory_string = reduce(lambda x, y: str(x) + '\n' + str(y)+ ' : ' + str(self.globalmemory[y]), self.globalmemory, '\n\nGlobal memory:')
            logfile = open("larrylog.txt","a")
            logfile.write(memory_string)
            logfile.close()
            return
        return self.evaluate(nodes, pos+1)