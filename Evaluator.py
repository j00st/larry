from Nodes import Node
from functools import reduce


class Evaluator(object):
    # __init__ :: None -> None
    def __init__(self) -> None:
        pass

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Evaluator'

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # evaluate :: Node -> {Tag, Node} -> Int -> None
    def evaluate(self, nodes: Node, globalmemory: dict = {}, pos: int = 0) -> None:
        node: Node = nodes[pos]
        node(globalmemory)
        if pos+1 >= len(nodes):
            memory_string = reduce(lambda x, y: str(x) + '\n' + str(y)+ ' : ' + str(globalmemory[y]), globalmemory, '\n\nGlobal memory:')
            logfile = open("larrylog.txt","a")
            logfile.write(memory_string)
            logfile.close()
            return
        return self.evaluate(nodes, globalmemory, pos+1)