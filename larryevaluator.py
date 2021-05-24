from larrynodes import Assignment, Comparison, Node, Constant, Tag, Operator, Operation


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
            return
        return self.evaluate(nodes, pos+1)
