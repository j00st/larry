from typing import List, Callable, Optional, Tuple, Dict


class Node(object):
    # __init__ :: None -> None
    def __init__(self) -> None:
        pass

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[{}}]'.format(None)

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # error :: String -> None
    def error(msg: str = 'unknown error'):
        raise Exception('Interpreter error: ' + msg)

    # log :: ({Tag, Node} -> Int -> None) -> ({Tag, Node} -> Int -> ({Tag, Node} -> Int -> None))
    def log(func: Callable) -> Callable:
        # inner :: {Tag, Node} -> Int -> ({Tag, Node} -> Int -> None)
        def inner(*args):
            logfile = open("larrylog.txt","a")
            logfile.write('\n' + func.__str__() + '\t\t' + str(args))
            logfile.close()
            return func(*args)
        return inner


class Constant(Node):
    # __init__ :: Int -> None
    def __init__(self, value: int) -> None:
        self.value: int = int(value)
    
    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Constant({})]'.format(self.value.__repr__())

    # __str__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()
    
    # __call__ :: {Tag, Node} -> Int
    def __call__(self, memory: Dict[Node, Node]) -> int:
        return self.value


class Tag(Node):
    # __init__ :: String -> Node -> None
    def __init__(self, name: str, value: Optional[Node] = None) -> None:
        self.name: str = name
        self.value: Optional[Node] = value
    
    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Tag({}, {})]'.format(self.name.__repr__(), self.value.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()
    
    # __call__ :: {Tag, Node} -> Int
    def __call__(self, memory: Dict[Node, Node]) -> int:
        if self.name in memory:
            self.value = memory[self.name]
        return self.value


class Operator(Node):
    # __init__ :: String -> None
    def __init__(self, op: str):
        self.op: str = op
    
    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Operator(%s)]' %(self.op.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Int
    def __call__(self, memory: Dict[Node, Node]) -> str:
        return self.op


class Operation(Node):
    # __init__ :: Node -> Operator -> Node -> None
    def __init__(self, left: Node, op: Operator, right: Node) -> None:
        self.left: Node = left
        self.op: Operator = op
        self.right: Node = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Operation(%s, %s, %s)]' %(self.left.__repr__(), self.op.__repr__(), self.right.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()
    
    # __call__ :: {Tag, Node} -> Int
    def __call__(self, memory: Dict[Node, Node]) -> int:
        if self.op(memory) == '+': return self.left(memory) + self.right(memory)
        elif self.op(memory) == '-': return self.left(memory) - self.right(memory)
        elif self.op(memory) == '*': return self.left(memory) * self.right(memory)
        elif self.op(memory) == '/': return self.left(memory) / self.right(memory)


class Comparison(Node):
    # __init__ :: Node -> Operator -> Node -> None
    def __init__(self, left: Node, op: Operator, right: Node) -> None:
        self.left: Node = left
        self.op: Operator = op
        self.right: Node = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Comparison(%s, %s, %s)]' %(self.left.__repr__(), self.op.__repr__(), self.right.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Bool
    def __call__(self, memory: Dict[Node, Node]) -> bool:
        if self.op(memory) == '<=': return self.left(memory) <= self.right(memory)
        elif self.op(memory) == '<': return self.left(memory) < self.right(memory)
        elif self.op(memory) == '>=': return self.left(memory) >= self.right(memory)
        elif self.op(memory) == '>': return self.left(memory) > self.right(memory)
        elif self.op(memory) == '!=': return self.left(memory) != self.right(memory)
        elif self.op(memory) == '==': return self.left(memory) == self.right(memory)


class Assignment(Node):
    # __init__ :: Node -> Node -> None
    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Assignment(%s, %s)]' %(self.left.__repr__(), self.right.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> None
    def __call__(self, memory: Dict[Node, Node]) -> None:
        memory[self.left.name] = self.right(memory)


class Print(Node):
    # __init__ :: Node -> None
    def __init__(self, body: Node) -> None:
        self.body: Node = body

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Print({})]'.format(self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> None
    def __call__(self, memory: Dict[Node, Node]) -> None:
        print(self.body(memory))


class Group(Node):
    # __init__ :: Node -> None
    def __init__(self, nodes) -> None:
        self.nodes: List[Node] = nodes

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Group({})]'.format(self.nodes.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Int -> Node
    def __call__(self, memory: Dict[Node, Node], pos: int = 0) -> Node:
        current_node: Node = self.nodes[pos]
        if(type(current_node) == Return):
            return current_node
        elif(len(self.nodes) == pos + 1):
            self.nodes[pos](memory)
            return
        elif(len(self.nodes) > pos):
            self.nodes[pos](memory)
            return self.__call__(memory, pos+1)


class If(Node):
    # __init__ :: Node -> Group -> None
    def __init__(self, condition: Node, body: Group) -> None:
        self.condition = condition
        self.body = body

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[If({}, {})]'.format(self.condition.__repr__(), self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Node
    def __call__(self, memory: Dict[Node, Node]) -> Node:
        if(self.condition(memory)):
            current_node = self.body(memory)
            if(type(current_node) == Return):
                return current_node


class While(Node):
    # __init__ :: Node -> Group -> None
    def __init__(self, condition: Node, body: Group) -> None:
        self.condition: Node = condition
        self.body: Group = body

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[While({}, {})]'.format(self.condition.__repr__(), self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Int -> None
    @Node.log
    def __call__(self, memory: Dict[Node, Node], pos: int = 0) -> None:
        if(self.condition(memory)):
            if(pos == len(self.body.nodes)):        # when last node is reached, set pos to first node (0)
                pos = 0
            current_node = self.body.nodes[pos](memory)
            if(type(current_node) == Return):
                return current_node
            self.__call__(memory, pos+1)


class Fun(Node):
    # __init__ :: Group -> [Node] -> None
    def __init__(self, body: Group, param: List[Node]) -> None:
        self.body: Group = body
        self.param: List[Node] = param

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Fun({}, {})]'.format(self.param.__repr__(), self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> [Node] -> {Tag, Node} -> Int -> Node | None
    @Node.log
    def __call__(self, memory: Dict[Node, Node], param: List[Node], function_memory: dict = {}, pos: int = 0) -> Optional[Node]:
        if(pos == 0):
            function_memory: List[Tuple[Node, Node]] = self.make_memory(memory, param)
        elif(pos == len(self.body.nodes)):
            return
        current_node = self.body.nodes[pos]
        if(type(current_node) == Return):
            return current_node(function_memory)
        ret = current_node(function_memory)
        if(type(ret) == Return):
            return current_node(function_memory)(function_memory)
        return self.__call__(memory, param, function_memory, pos+1)
    
    # make_memory :: {Tag, Node} -> [Node] -> {Tag, Node} -> Int -> [Node]
    def make_memory(self, memory: Dict[Node, Node], param: List[Node], function_memory: Dict[Node, Node] = {}, pos: int = 0) -> List[Node]:
        if(len(param) == pos):
            function_memory.update(memory)
            return function_memory
        function_memory[self.param[pos].name] = param[pos](memory)
        return self.make_memory(memory, param, function_memory, pos+1)


class FunDec(Node):
    # __init__ :: Group -> [Node] -> None
    def __init__(self, body: Group, param: List[Node]) -> None:
        self.body: Group = body
        self.param: List[Node] = param

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[FunDec({}, {})]'.format(self.body.__repr__(), self.param.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Int -> Fun
    def __call__(self, memory: dict, pos: int = 0) -> Fun:
        return Fun(self.body, self.param)


class Run(Node):
    # __init__ :: Tag -> [Node] -> None
    def __init__(self, name: Tag, param: List[Node]) -> None:
        self.name: Tag = name
        self.param: List[Node] = param

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Run({}, {})]'.format(self.name.__repr__(), self.param.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Fun
    def __call__(self, memory: dict) -> Fun:
        return memory[self.name.name](memory, self.param)


class Return(Node):
    # __init__ :: Node -> None
    def __init__(self, body: Node) -> None:
        self.body: Node = body

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Return({})]'.format(self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Node
    def __call__(self, memory: dict) -> Node:
        return self.body(memory)