from Nodes import Node
from functools import reduce
from typing import List


"""
class Evaluator: Funcitonality calls all root Nodes in order to run the AST
"""
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

    """
    evaluate :: [Node] -> {Tag, Node} -> Int -> None

    The evaluate function takes a list of Nodes and calls every Nodes __call__
    function. It also creates an empty memory dictionary that is passed to each
    Node. At the end of the evaluation process, the memory is written to the
    logfile.
    """
    def evaluate(self, nodes: List[Node], globalmemory: dict = {}, \
        pos: int = 0) -> None:
        node: Node = nodes[pos]
        # Call the Nodes __call__ function to which will execute what the Node
        # is meant to do
        node(globalmemory)
        if pos+1 >= len(nodes):
            memory_string = reduce(lambda x, y: str(x) + '\n' + str(y) + ' : ' \
                + str(globalmemory[y]), globalmemory, '\n\nGlobal memory:')
            logfile = open("larrylog.txt","a")
            logfile.write(memory_string)
            logfile.close()
            return None
        return self.evaluate(nodes, globalmemory, pos+1)