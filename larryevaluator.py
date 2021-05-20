from larrynodes import Assignment, Comparison, Node, Constant, Tag, Operator, Operation

class Evaluator(object):
    def __init__(self) -> None:
        self.globalmemory = {}

    def __str__(self) -> str:
        return 'Evaluator'

    def __repr__(self) -> str:
        return self.__str__()
    
    # def operation(self, node: Operation) -> None:
    #     print(node())
    
    # def comparison(self, node: Comparison) -> None:
    #     print(node())
    
    # def assignment(self, node: Assignment) -> Tag:
    #     print(node())

    def evaluate(self, nodes: Node, pos: int = 0) -> None:
        node = nodes[pos]
        node(self.globalmemory)
        if pos+1 >= len(nodes):
            return
        return self.evaluate(nodes, pos+1)
