from typing import List, Callable, Optional, Tuple, Dict


"""
class Node: The parent class all Nodes inherit from

Contains basic functionality like error handling.
"""
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

    """
    log :: ({Tag, Node} -> Int -> None) -> ({Tag, Node} -> Int -> 
           ({Tag, Node} -> Int -> None))

    This function can be used to decorate any child of Node's __call__ function
    with. It logs the function's name and location in the memory to the logfile.
    """
    def log(func: Callable) -> Callable:
        # inner :: {Tag, Node} -> Int -> ({Tag, Node} -> Int -> None)
        def inner(*args):
            logfile = open("larrylog.txt","a")
            logfile.write('\n' + func.__str__() + '\t\t' + str(args))
            logfile.close()
            return func(*args)
        return inner


"""
class Constant: For objects containing a constant value

Any integer value is stored in a Constant object.
"""
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


"""
class Tag: For objects containing a tag and possibly its accompanying value
"""
class Tag(Node):
    # __init__ :: String -> Node -> None
    def __init__(self, name: str, value: Optional[Node] = None) -> None:
        self.name: str = name
        self.value: Optional[Node] = value
    
    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Tag({}, {})]'.format(self.name.__repr__(), \
            self.value.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()
    
    # __call__ :: {Tag, Node} -> Int
    def __call__(self, memory: Dict[Node, Node]) -> int:
        if self.name in memory:
            self.value = memory[self.name]
        return self.value


"""
class Operator: For objects containing an operator
"""
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


"""
class Operation: For objects containing an operation

Operations consist of a left node, an operator, and a right node. Left and right
nodes can be parent nodes of more operations or a comparison.
"""
class Operation(Node):
    # __init__ :: Node -> Operator -> Node -> None
    def __init__(self, left: Node, op: Operator, right: Node) -> None:
        self.left: Node = left
        self.op: Operator = op
        self.right: Node = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Operation(%s, %s, %s)]' %(self.left.__repr__(), \
            self.op.__repr__(), self.right.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()
    
    # __call__ :: {Tag, Node} -> Int
    def __call__(self, memory: Dict[Node, Node]) -> int:
        if self.op(memory) == '+': return self.left(memory) + \
                                          self.right(memory)
        elif self.op(memory) == '-': return self.left(memory) - \
                                            self.right(memory)
        elif self.op(memory) == '*': return self.left(memory) * \
                                            self.right(memory)
        elif self.op(memory) == '/': 
            right = self.left(memory)
            if self.right(memory) == 0:
                Node.error('Devision by zero not allowed')
            return self.left(memory) / right


"""
class Comparison: For objects containing a comparison

Comparisons consist of a left Node, an operator and a right Node. Left and right
Nodes can be parent nodes of Operations.
"""
class Comparison(Node):
    # __init__ :: Node -> Operator -> Node -> None
    def __init__(self, left: Node, op: Operator, right: Node) -> None:
        self.left: Node = left
        self.op: Operator = op
        self.right: Node = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Comparison(%s, %s, %s)]' %(self.left.__repr__(), \
            self.op.__repr__(), self.right.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Bool
    def __call__(self, memory: Dict[Node, Node]) -> bool:
        if self.op(memory) == '<=': return self.left(memory) <= \
                                           self.right(memory)
        elif self.op(memory) == '<': return self.left(memory) < \
                                            self.right(memory)
        elif self.op(memory) == '>=': return self.left(memory) >= \
                                             self.right(memory)
        elif self.op(memory) == '>': return self.left(memory) > \
                                            self.right(memory)
        elif self.op(memory) == '!=': return self.left(memory) != \
                                             self.right(memory)
        elif self.op(memory) == '==': return self.left(memory) == \
                                             self.right(memory)


"""
class Assignment: For objects containing an assignment

Assignment nodes consist of a left Tag Node and a right Node. When called, the
value of the right Node is assigned to the Tag Node on the left.
"""
class Assignment(Node):
    # __init__ :: Tag -> Node -> None
    def __init__(self, left: Tag, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Assignment(%s, %s)]' %(self.left.__repr__(), \
            self.right.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> None
    def __call__(self, memory: Dict[Node, Node]) -> None:
        memory[self.left.name] = self.right(memory)


"""
class Print: For objects containing a Print statement

Print objects contain a Node called body. The body is executed and its result is
returned to the terminal.
"""
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


"""
class Group: For objects containing a group of Nodes

To enable If, While and generic functions groups of Nodes can be made. The Group
Node object contains a group of Nodes which will each be called when the Group
Node is called.
"""
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


"""
class If: For objects containing an If statement

This object contains a condition Node and a body Group. When executed, it checks
whether the condition returns True and if True it executes the Group Node.
"""
class If(Node):
    # __init__ :: Node -> Group -> None
    def __init__(self, condition: Node, body: Group) -> None:
        self.condition = condition
        self.body = body

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[If({}, {})]'.format(self.condition.__repr__(), \
            self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Node
    def __call__(self, memory: Dict[Node, Node]) -> Node:
        if(self.condition(memory)):
            current_node = self.body(memory)
            # Return Nodes can be found in If statements when inside a Function
            if(type(current_node) == Return):
                return current_node


"""
class While: For objects containing a While statement

The While object consists of a condition Node and a body Group. It keeps
executing the Group Node's Nodes as long as the condition Node's execution
returns True. The condition is also checked while executing the Group Node, like
in most programming languages.
"""
class While(Node):
    # __init__ :: Node -> Group -> None
    def __init__(self, condition: Node, body: Group) -> None:
        self.condition: Node = condition
        self.body: Group = body

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[While({}, {})]'.format(self.condition.__repr__(), \
            self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Int -> None
    @Node.log
    def __call__(self, memory: Dict[Node, Node], pos: int = 0) -> None:
        if(self.condition(memory)):
            if(pos == len(self.body.nodes)):
                pos = 0
            # The While Node calls the Group Nodes' body itself in order to
            # check the condition between every call
            current_node = self.body.nodes[pos](memory)
            # Return Nodes can be found in While loops when inside a Function
            if(type(current_node) == Return):
                return current_node
            self.__call__(memory, pos+1)


"""
class Fun: For objects containing a Function

The Function Node contains its body as a Group Node and its parameters as a list
of Nodes. When called, the parameters are added to its memory and its body is
executed.
"""
class Fun(Node):
    # __init__ :: Group -> [Node] -> None
    def __init__(self, body: Group, param: List[Node]) -> None:
        self.body: Group = body
        self.param: List[Node] = param

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Fun({}, {})]'.format(self.param.__repr__(), \
            self.body.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> [Node] -> {Tag, Node} -> Int -> Node | None
    @Node.log
    def __call__(self, memory: Dict[Node, Node], param: List[Node], \
        function_memory: dict = {}, pos: int = 0) -> Optional[Node]:
        if(pos == 0):
            # Create a new memory dictionary for the function
            function_memory: List[Tuple[Node, Node]] = \
                self.make_memory(memory, param)
        # Base case - when no Return value found return None
        elif(pos == len(self.body.nodes)):
            return None
        current_node = self.body.nodes[pos]
        if(type(current_node) == Return):
            return current_node(function_memory)
        ret = current_node(function_memory)
        if(type(ret) == Return):
            return current_node(function_memory)(function_memory)
        return self.__call__(memory, param, function_memory, pos+1)
    
    """
    make_memory :: {Tag, Node} -> [Node] -> {Tag, Node} -> Int -> [Node]

    This function is called by the Functions __call__ method. It puts the
    parameters in a new dictionary and adds the global memory to the dictionary
    making sure it knows all global variables and functions, including itself.
    """
    def make_memory(self, memory: Dict[Node, Node], param: List[Node], \
        function_memory: Dict[Node, Node] = {}, pos: int = 0) -> List[Node]:
        if(len(param) == pos):
            # Add the global memory to the functions memory
            function_memory.update(memory)
            return function_memory
        function_memory[self.param[pos].name] = param[pos](memory)
        return self.make_memory(memory, param, function_memory, pos+1)


"""
class FunDec: For objects containing a Function Decleration

When a function is declared in the code, a Function Decleration Node is created.
When called, it returns a Function Node, which will be stored in the memory.
"""
class FunDec(Node):
    # __init__ :: Group -> [Node] -> None
    def __init__(self, body: Group, param: List[Node]) -> None:
        self.body: Group = body
        self.param: List[Node] = param

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[FunDec({}, {})]'.format(self.body.__repr__(), \
            self.param.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Int -> Fun
    def __call__(self, memory: dict, pos: int = 0) -> Fun:
        return Fun(self.body, self.param)


"""
class Run: For objects containing a Run statement

A function can be called with the Run Node which will finally execute the
functions body.
"""
class Run(Node):
    # __init__ :: Tag -> [Node] -> None
    def __init__(self, name: Tag, param: List[Node]) -> None:
        self.name: Tag = name
        self.param: List[Node] = param

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Node[Run({}, {})]'.format(self.name.__repr__(), \
            self.param.__repr__())

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # __call__ :: {Tag, Node} -> Fun
    def __call__(self, memory: dict) -> Fun:
        return memory[self.name.name](memory, self.param)


"""
class Return: For objects containing a Return statement

The Return object contains a Node as body which' return value will be returned
when the object is called by the Function Node.
"""
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