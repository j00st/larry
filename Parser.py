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


class Parser(object):
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.pos = 0

    def __str__(self) -> str:
        return 'Parser'

    def __repr__(self) -> str:
        return self.__str__()
    
    def error(self):
        raise Exception('Parser error')

    def advance(self, *args):
        token = self.tokens[self.pos]
        if token.type in args or token.value in args:
            self.pos += 1
        else:
            self.error()

    def int_tag(self):
        token = self.tokens[self.pos]
        if token.type == 't_INT':
            self.advance('t_INT')
            return Constant(token.value)
        elif token.type == 't_TAG':
            self.advance('t_TAG')
            return Tag(token.value, None)
        elif token.type == 't_LPAR':
            self.advance('t_LPAR')
            node = self.compare()
            self.advance('t_RPAR')
            return node
        self.error()
    
    def mul_div(self, node = None):
        if not node:
            node = self.int_tag()
        token = self.tokens[self.pos]
        if (token.value == '*') | (token.value == '/'):
            self.advance('*', '/')
            node = Operation(node, Operator(token.value), self.int_tag())
        else:
            return node
        return self.mul_div(node)
        
    def plu_min(self, node = None):
        if not node:
            node = self.mul_div()
        token = self.tokens[self.pos]
        if (token.value == '+') | (token.value == '-'):
            self.advance('+', '-')
            node = Operation(node, Operator(token.value), self.mul_div())
        else:
            return node
        return self.plu_min(node)

    def compare(self):
        node = self.plu_min()
        token = self.tokens[self.pos]
        if token.type == 't_COMP':
            self.advance('t_COMP')
            node = Comparison(node, Operator(token.value), self.plu_min())
        return node

    def assign(self):
        node = self.compare()
        token = self.tokens[self.pos]
        if token.type == 't_ASSIGN':
            self.advance('t_ASSIGN')
            node = Assignment(node, self.begin())
        return node

    def print(self):
        token = self.tokens[self.pos]
        if token.type == 't_PRINTFUN':
            self.advance('t_PRINTFUN')
            node = Print(self.begin())
            return node
        return self.assign()
    
    def if_fun(self):
        token = self.tokens[self.pos]
        if token.type == 't_IFFUN':
            self.advance('t_IFFUN')
            condition = self.compare()
            self.advance('t_COLON')
            self.advance('t_ENDOFLINE')
            node = If(condition, self.group([]))
            return node
        return self.print()

    def while_fun(self):
        token = self.tokens[self.pos]
        if token.type == 't_WHILEFUN':
            self.advance('t_WHILEFUN')
            condition = self.compare()
            self.advance('t_COLON')
            self.advance('t_ENDOFLINE')
            node = While(condition, self.group([]))
            return node
        return self.if_fun()

    def param_fun(self):
        token = self.tokens[self.pos]
        if token.type == 't_PARAMFUN':
            self.advance('t_PARAMFUN')
            param = self.collect_param([])
            self.advance('t_COLON')
            self.advance('t_ENDOFLINE')
            node = FunDec(self.group([]), param)
            return node
        return self.while_fun()
    
    def run(self):
        token = self.tokens[self.pos]
        if token.type == 't_RUN':
            self.advance('t_RUN')
            node = Run(self.int_tag(), self.collect_param([]))
            return node
        return self.param_fun()
    
    def fun_return(self):
        token = self.tokens[self.pos]
        if token.type == 't_RETURN':
            self.advance('t_RETURN')
            node = Return(self.begin())
            return node
        return self.run()

    def begin(self):
        return self.fun_return()

    def collect_param(self, nodes: Node = []):
        token = self.tokens[self.pos]
        if(token.type in ('t_ENDOFLINE', 't_EOF', 't_COLON')):
            return nodes
        if(token.value == '>'):
            self.advance('>')
            nodes.append(self.plu_min())
            return self.collect_param(nodes)
        self.error()
    
    def group(self, nodes = []):
        node = self.begin()
        token = self.tokens[self.pos]
        if token.type == 't_ENDOFLINE':
            self.advance('t_ENDOFLINE')
            nodes.append(node)
            token = self.tokens[self.pos]
            if token.type == 't_ENDFUN':
                self.advance('t_ENDFUN')
                return Group(nodes)
        return self.group(nodes)

    def log(self, nodes: list, pos: int = 0) -> None:
        if(pos<len(nodes)):
            logfile = open("larrylog.txt","a")
            logfile.write('\n' + str(nodes[pos]))
            logfile.close()
            return self.log(nodes, pos+1)
        logfile = open("larrylog.txt","a")
        logfile.write('\n\nLoop and function calls:\t\t\t\t\tWith arguments:')
        logfile.close()

    def parse(self, nodes = []):
        node = self.begin()
        token = self.tokens[self.pos]
        if token.type == 't_ENDOFLINE':
            self.advance('t_ENDOFLINE')
            nodes.append(node)
        if token.type == 't_EOF':
            nodes.append(node)
            self.log(nodes)
            return nodes
        return self.parse(nodes)