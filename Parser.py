from Nodes import Constant, \
                       Node, \
                       Tag, \
                       Operator, \
                       Operation, \
                       Comparison, \
                       Assignment, \
                       Print, \
                       If, \
                       Group, \
                       While, \
                       FunDec, \
                       Run, \
                       Return
from Lexer import Token
from typing import List, Optional


class Parser(object):
    # __init__ :: [Token] -> None
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens: List[Token] = tokens
        self.pos: int = 0

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Parser'

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()
    
    # error :: String -> None
    def error(self):
        raise Exception('Parser error')

    # advance :: String -> None
    def advance(self, *args: str) -> None:
        token: Token = self.tokens[self.pos]
        if token.type in args or token.value in args:
            self.pos += 1
        else:
            self.error()

    # int_tag :: None -> Node
    def int_tag(self) -> Optional[Node]:
        token: Token = self.tokens[self.pos]
        if token.type == 't_INT':
            self.advance('t_INT')
            return Constant(token.value)
        elif token.type == 't_TAG':
            self.advance('t_TAG')
            return Tag(token.value, None)
        elif token.type == 't_LPAR':
            self.advance('t_LPAR')
            node: Node = self.compare()
            self.advance('t_RPAR')
            return node
        self.error()
    
    # mul_div :: Node -> Node
    def mul_div(self, node: Optional[Node] = None) -> Node:
        if not node:
            node: Node = self.int_tag()
        token: Token = self.tokens[self.pos]
        if (token.value == '*') | (token.value == '/'):
            self.advance('*', '/')
            node: Node = Operation(node, Operator(token.value), self.int_tag())
        else:
            return node
        return self.mul_div(node)
        
    # plu_min :: Node -> Node
    def plu_min(self, node: Optional[Node] = None) -> Node:
        if not node:
            node: Node = self.mul_div()
        token: Token = self.tokens[self.pos]
        if (token.value == '+') | (token.value == '-'):
            self.advance('+', '-')
            node: Node = Operation(node, Operator(token.value), self.mul_div())
        else:
            return node
        return self.plu_min(node)

    # compare :: None -> Node
    def compare(self) -> Node:
        node: Node = self.plu_min()
        token: Token = self.tokens[self.pos]
        if token.type == 't_COMP':
            self.advance('t_COMP')
            node: Node = Comparison(node, Operator(token.value), self.plu_min())
        return node

    # assign :: None -> Node
    def assign(self) -> Node:
        node: Node = self.compare()
        token: Token = self.tokens[self.pos]
        if token.type == 't_ASSIGN':
            self.advance('t_ASSIGN')
            node: Node = Assignment(node, self.begin())
        return node

    # print :: None -> Node
    def print(self) -> Node:
        token: Token = self.tokens[self.pos]
        if token.type == 't_PRINTFUN':
            self.advance('t_PRINTFUN')
            node: Node = Print(self.begin())
            return node
        return self.assign()
    
    # if_fun :: None -> Node
    def if_fun(self) -> Node:
        token: Token = self.tokens[self.pos]
        if token.type == 't_IFFUN':
            self.advance('t_IFFUN')
            condition = self.compare()
            self.advance('t_COLON')
            self.advance('t_ENDOFLINE')
            node: Node = If(condition, self.group([]))
            return node
        return self.print()

    # while_fun :: None -> Node
    def while_fun(self) -> Node:
        token: Token = self.tokens[self.pos]
        if token.type == 't_WHILEFUN':
            self.advance('t_WHILEFUN')
            condition = self.compare()
            self.advance('t_COLON')
            self.advance('t_ENDOFLINE')
            node: Node = While(condition, self.group([]))
            return node
        return self.if_fun()

    # param_fun :: None -> Node
    def param_fun(self) -> Node:
        token: Token = self.tokens[self.pos]
        if token.type == 't_PARAMFUN':
            self.advance('t_PARAMFUN')
            param = self.collect_param([])
            self.advance('t_COLON')
            self.advance('t_ENDOFLINE')
            node: Node = FunDec(self.group([]), param)
            return node
        return self.while_fun()
    
    # run :: None -> Node
    def run(self) -> Node:
        token: Token = self.tokens[self.pos]
        if token.type == 't_RUN':
            self.advance('t_RUN')
            node: Node = Run(self.int_tag(), self.collect_param([]))
            return node
        return self.param_fun()
    
    # fun_return :: None -> Node
    def fun_return(self) -> Node:
        token: Token = self.tokens[self.pos]
        if token.type == 't_RETURN':
            self.advance('t_RETURN')
            node: Node = Return(self.begin())
            return node
        return self.run()

    # begin :: None -> Node
    def begin(self) -> Node:
        return self.fun_return()

    # collect_param :: [Node] -> [Node]
    def collect_param(self, nodes: List[Node] = []) -> Optional[List[Node]]:
        token: Token = self.tokens[self.pos]
        if(token.type in ('t_ENDOFLINE', 't_EOF', 't_COLON')):
            return nodes
        if(token.value == '>'):
            self.advance('>')
            nodes.append(self.plu_min())
            return self.collect_param(nodes)
        self.error()
    
    # group :: [None] -> Node
    def group(self, nodes: List[Node] = []) -> Node:
        node: Node = self.begin()
        token: Token = self.tokens[self.pos]
        if token.type == 't_ENDOFLINE':
            self.advance('t_ENDOFLINE')
            nodes.append(node)
            token = self.tokens[self.pos]
            if token.type == 't_ENDFUN':
                self.advance('t_ENDFUN')
                return Group(nodes)
        return self.group(nodes)

    # int_tag :: [None] -> Int -> None
    def log(self, nodes: List[Node], pos: int = 0) -> None:
        if(pos == 0):
            nodes = list(map((lambda x: str(nodes.index(x)) + '\t' + str(x)), nodes))
        if(pos<len(nodes)):
            logfile = open("larrylog.txt","a")
            logfile.write('\n' + str(nodes[pos]))
            logfile.close()
            return self.log(nodes, pos+1)
        logfile = open("larrylog.txt","a")
        logfile.write('\n\nLoop and function calls:\t\t\t\t\tWith arguments:')
        logfile.close()

    # int_tag :: [None] -> [Node]
    def parse(self, nodes: List[Node] = []) -> List[Node]:
        node: Node = self.begin()
        token: Token = self.tokens[self.pos]
        if token.type == 't_ENDOFLINE':
            self.advance('t_ENDOFLINE')
            nodes.append(node)
        if token.type == 't_EOF':
            nodes.append(node)
            self.log(nodes)
            return nodes
        return self.parse(nodes)