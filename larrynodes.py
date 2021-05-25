from typing import List


class Node(object):
    def __init__(self) -> None:
        pass

    def log(func):
        def inner(*args):
            logfile = open("larrylog.txt","a")
            logfile.write('\n' + func.__str__() + '\t\t' + str(args))
            logfile.close()
            return func(*args)
        return inner


class Constant(Node):
    def __init__(self, value):
        self.value = int(value)
    
    def __str__(self) -> str:
        return 'Node[Constant({})]'.format(self.value)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __call__(self, memory: dict) -> int:
        return self.value


class Tag(Node):
    def __init__(self, name: str, value: Node = None) -> None:
        self.name = name
        self.value = value
    
    def __str__(self) -> str:
        return 'Node[Tag({}, {})]'.format(self.name, self.value)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __call__(self, memory: dict):
        if self.name in memory:
            self.value = memory[self.name]
        return self.value


class Operator(Node):
    def __init__(self, op):
        self.op = op
    
    def __str__(self) -> str:
        return 'Node[Operator(%s)]' %(self.op)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict) -> str:
        return self.op


class Operation(Node):
    def __init__(self, left: Node, op: Operator, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return 'Node[Operation(%s, %s, %s)]' %(self.left, self.op, self.right)

    def __repr__(self) -> str:
        return self.__str__()
    
    def __call__(self, memory: dict) -> int:
        if self.op(memory) == '+': return self.left(memory) + self.right(memory)
        elif self.op(memory) == '-': return self.left(memory) - self.right(memory)
        elif self.op(memory) == '*': return self.left(memory) * self.right(memory)
        elif self.op(memory) == '/': return self.left(memory) / self.right(memory)


class Comparison(Node):
    def __init__(self, left: Node, op: Operator, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return 'Node[Comparison(%s, %s, %s)]' %(self.left, self.op, self.right)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict) -> bool:
        if self.op(memory) == '<=': return self.left(memory) <= self.right(memory)
        elif self.op(memory) == '<': return self.left(memory) < self.right(memory)
        elif self.op(memory) == '>=': return self.left(memory) >= self.right(memory)
        elif self.op(memory) == '>': return self.left(memory) > self.right(memory)
        elif self.op(memory) == '!=': return self.left(memory) != self.right(memory)
        elif self.op(memory) == '==': return self.left(memory) == self.right(memory)


class Assignment(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return 'Node[Assignment(%s, %s)]' %(self.left, self.right)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict) -> None:
        memory[self.left.name] = self.right(memory)


class Print(Node):
    def __init__(self, body: Node):
        self.body = body

    def __str__(self) -> str:
        return 'Node[Print({})]'.format(self.body)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict) -> None:
        print(self.body(memory))


class Group(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self) -> str:
        return 'Node[Group({})]'.format(self.nodes)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict, pos: int = 0) -> Node:
        current_node = self.nodes[pos]
        if(type(current_node) == Return):
            return current_node
        elif(len(self.nodes) == pos + 1):
            self.nodes[pos](memory)
            return
        elif(len(self.nodes) > pos):
            self.nodes[pos](memory)
            return self.__call__(memory, pos+1)


class If(Node):
    def __init__(self, condition: Node, body: Group):
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return 'Node[If({}, {})]'.format(self.condition, self.body)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict) -> Node:
        if(self.condition(memory)):
            current_node = self.body(memory)
            if(type(current_node) == Return):
                return current_node


class While(Node):
    def __init__(self, condition: Node, body: Group):
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return 'Node[While({}, {})]'.format(self.condition, self.body)

    def __repr__(self) -> str:
        return self.__str__()

    @Node.log
    def __call__(self, memory: dict, pos=0) -> None:
        if(self.condition(memory)):
            if(pos == len(self.body.nodes)):        # when last node is reached, set pos to first node (0)
                pos=0
            current_node = self.body.nodes[pos](memory)
            if(type(current_node) == Return):
                return current_node
            self.__call__(memory, pos+1)


class Fun(Node):
    def __init__(self, body: Group, param: list):
        self.body = body
        self.param = param

    def __str__(self) -> str:
        return 'Node[Fun({}, {})]'.format(self.param, self.body)

    def __repr__(self) -> str:
        return self.__str__()

    @Node.log
    def __call__(self, memory: dict, param: list, function_memory: dict = {}, pos: int = 0) -> Node:
        if(pos == 0):
            function_memory = self.make_memory(memory, param)
        elif(pos == len(self.body.nodes)):
            return
        current_node = self.body.nodes[pos]
        if(type(current_node) == Return):
            return current_node(function_memory)
        ret = current_node(function_memory)
        if(type(ret) == Return):
            return current_node(function_memory)(function_memory)
        return self.__call__(memory, param, function_memory, pos+1)
    
    def make_memory(self, memory: dict, param: list, function_memory: dict = {}, pos: int = 0) -> list:
        if(len(param) == pos):
            function_memory.update(memory)
            return function_memory
        function_memory[self.param[pos].name] = param[pos](memory)
        return self.make_memory(memory, param, function_memory, pos+1)


class FunDec(Node):
    def __init__(self, body: Group, param: list):
        self.body = body
        self.param = param

    def __str__(self) -> str:
        return 'Node[FunDec({}, {})]'.format(self.body, self.param)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict, pos=0) -> Fun:
        return Fun(self.body, self.param)


class Run(Node):
    def __init__(self, name: Tag, param: list):
        self.name = name
        self.param = param

    def __str__(self) -> str:
        return 'Node[Run({}, {})]'.format(self.name, self.param)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict) -> Node:
        return memory[self.name.name](memory, self.param)


class Return(Node):
    def __init__(self, body: Node):
        self.body = body

    def __str__(self) -> str:
        return 'Node[Return({})]'.format(self.body)

    def __repr__(self) -> str:
        return self.__str__()

    def __call__(self, memory: dict) -> None:
        return self.body(memory)