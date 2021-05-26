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
    # __init__ :: None -> None
    def __init__(self) -> None:
        pass

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Parser'

    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()
    
    # error :: String -> None
    def error(self):
        raise Exception('Parser error')

    # advance :: [Token] -> String -> [Token]
    def advance(self, tokens: List[Token], *args: str) -> Optional[List[Token]]:
        head, *tail = tokens
        if head.type in args or head.value in args:
            return tail
        else:
            self.error()

    # int_tag :: [Token] -> Node
    def int_tag(self, tokens: List[Token]) -> Optional[Node]:
        token: Token = tokens[0]
        if token.type == 't_INT':
            tokens = self.advance(tokens, 't_INT')
            return tokens, Constant(token.value)
        elif token.type == 't_TAG':
            tokens = self.advance(tokens, 't_TAG')
            return tokens, Tag(token.value, None)
        elif token.type == 't_LPAR':
            tokens = self.advance(tokens, 't_LPAR')
            tokens, node = self.compare(tokens)
            tokens = self.advance(tokens, 't_RPAR')
            return tokens, node
        self.error()
    
    # mul_div :: Node -> Node
    def mul_div(self, tokens: List[Token], node: Optional[Node] = None) -> Node:
        if not node:
            tokens, node = self.int_tag(tokens)
        token: Token = tokens[0]
        if (token.value == '*') | (token.value == '/'):
            tokens = self.advance(tokens, '*', '/')
            tokens, right = self.int_tag(tokens)
            node = Operation(node, Operator(token.value), right)
        else:
            return tokens, node
        return self.mul_div(tokens, node)
        
    # plu_min :: Node -> Node
    def plu_min(self, tokens: List[Token], node: Optional[Node] = None) -> Node:
        if not node:
            tokens, node = self.mul_div(tokens)
        token: Token = tokens[0]
        if (token.value == '+') | (token.value == '-'):
            tokens = self.advance(tokens, '+', '-')
            tokens, right = self.mul_div(tokens)
            node = Operation(node, Operator(token.value), right)
        else:
            return tokens, node
        return self.plu_min(tokens, node)

    # compare :: None -> Node
    def compare(self, tokens: List[Token]) -> Node:
        tokens, node = self.plu_min(tokens)
        token: Token = tokens[0]
        if token.type == 't_COMP':
            tokens = self.advance(tokens, 't_COMP')
            tokens, right = self.plu_min(tokens)
            node = Comparison(node, Operator(token.value), right)
        return tokens, node

    # assign :: None -> Node
    def assign(self, tokens: List[Token]) -> Node:
        tokens, node = self.compare(tokens)
        token: Token = tokens[0]
        if token.type == 't_ASSIGN':
            tokens = self.advance(tokens, 't_ASSIGN')
            tokens, body = self.begin(tokens)
            node = Assignment(node, body)
        return tokens, node

    # print :: None -> Node
    def print(self, tokens: List[Token]) -> Node:
        token: Token = tokens[0]
        if token.type == 't_PRINTFUN':
            tokens = self.advance(tokens, 't_PRINTFUN')
            tokens, body = self.begin(tokens)
            node = Print(body)
            return tokens, node
        return self.assign(tokens)
    
    # if_fun :: None -> Node
    def if_fun(self, tokens: List[Token]) -> Node:
        token: Token = tokens[0]
        if token.type == 't_IFFUN':
            tokens = self.advance(tokens, 't_IFFUN')
            tokens, condition = self.compare(tokens)
            tokens = self.advance(tokens, 't_COLON')
            tokens = self.advance(tokens, 't_ENDOFLINE')
            tokens, body = self.group(tokens, [])
            node = If(condition, body)
            return tokens, node
        return self.print(tokens)

    # while_fun :: None -> Node
    def while_fun(self, tokens: List[Token]) -> Node:
        token: Token = tokens[0]
        if token.type == 't_WHILEFUN':
            tokens = self.advance(tokens, 't_WHILEFUN')
            tokens, condition = self.compare(tokens)
            tokens = self.advance(tokens, 't_COLON')
            tokens = self.advance(tokens, 't_ENDOFLINE')
            tokens, body = self.group(tokens, [])
            node = While(condition, body)
            return tokens, node
        return self.if_fun(tokens)

    # param_fun :: None -> Node
    def param_fun(self, tokens: List[Token]) -> Node:
        token: Token = tokens[0]
        if token.type == 't_PARAMFUN':
            tokens = self.advance(tokens, 't_PARAMFUN')
            tokens, param = self.collect_param(tokens, [])
            tokens = self.advance(tokens, 't_COLON')
            tokens = self.advance(tokens, 't_ENDOFLINE')
            tokens, body = self.group(tokens, [])
            node = FunDec(body, param)
            return tokens, node
        return self.while_fun(tokens)
    
    # run :: None -> Node
    def run(self, tokens: List[Token]) -> Node:
        token: Token = tokens[0]
        if token.type == 't_RUN':
            tokens = self.advance(tokens, 't_RUN')
            tokens, name = self.int_tag(tokens)
            tokens, param = self.collect_param(tokens, [])
            node = Run(name, param)
            return tokens, node
        return self.param_fun(tokens)
    
    # fun_return :: None -> Node
    def fun_return(self, tokens: List[Token]) -> Node:
        token: Token = tokens[0]
        if token.type == 't_RETURN':
            tokens = self.advance(tokens, 't_RETURN')
            tokens, body = self.begin(tokens)
            node = Return(body)
            return tokens, node
        return self.run(tokens)

    # begin :: None -> Node
    def begin(self, tokens: List[Token]) -> Node:
        return self.fun_return(tokens)

    # collect_param :: [Node] -> [Node]
    def collect_param(self, tokens: List[Token], nodes: List[Node] = []) -> Optional[List[Node]]:
        token: Token = tokens[0]
        if(token.type in ('t_ENDOFLINE', 't_EOF', 't_COLON')):
            return tokens, nodes
        if(token.value == '>'):
            tokens = self.advance(tokens, '>')
            tokens, node = self.plu_min(tokens)
            nodes.append(node)
            return self.collect_param(tokens, nodes)
        self.error()
    
    # group :: [None] -> Node
    def group(self, tokens: List[Token], nodes: List[Node] = []) -> Node:
        tokens, node = self.begin(tokens)
        token: Token = tokens[0]
        if token.type == 't_ENDOFLINE':
            tokens = self.advance(tokens, 't_ENDOFLINE')
            nodes.append(node)
            token = tokens[0]
            if token.type == 't_ENDFUN':
                tokens = self.advance(tokens, 't_ENDFUN')
                return tokens, Group(nodes)
        return self.group(tokens, nodes)

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
    def parse(self, tokens: List[Token], nodes: List[Node] = []) -> List[Node]:
        tokens, node = self.begin(tokens)
        token: Token = tokens[0]
        if token.type == 't_ENDOFLINE':
            tokens = self.advance(tokens, 't_ENDOFLINE')
            nodes.append(node)
        if token.type == 't_EOF':
            nodes.append(node)
            self.log(nodes)
            return nodes
        return self.parse(tokens, nodes)