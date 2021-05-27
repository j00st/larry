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
from typing import Callable, List, Optional, Tuple


"""
class Parser: Funcitonality mainly takes Tokens from the Lexer and produces
Nodes for the Evaluator

The Tokens passed on through functions which will return Nodes when appropriate.
The order of the functions dictates the precedence of operators and keywords
which will make the AST respect proper grammar rules. Tokens are 'consumed' when
the appropriate Node is created, moving on to the next Token. When all Tokens
are 'consumed', the Nodes are returned so that the Evaluator kan call their
respective functions.
"""
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

    """
    advance :: [Token] -> String -> [Token]

    The advance function takes the token list and information about the expected
    token and, if the information is correct, returns a new token list where
    the 'found' token is 'consumed', or, removed.
    """
    def advance(self, tokens: List[Token], *args: str) -> Optional[List[Token]]:
        head, *tail = tokens
        # It's both possible to check against the token type and token value
        if head.type in args or head.value in args:
            return tail
        else:
            self.error()

    """
    int_tag :: [Token] -> ([Token], Node)

    When this function is called, it checks if an integer constant, a tag (a
    variable or function name) or a set of paranthesis can be found.
    """
    def int_tag(self, tokens: List[Token]) -> \
        Optional[Tuple[List[Token], Node]]:
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
    
    """
    mul_div :: [Token] -> Node -> ([Token], Node)

    When this function is called, it checks if a multiplication or division 
    operator can be found. If not, continue to call the function int_tag.
    """
    def mul_div(self, tokens: List[Token], node: Optional[Node] = None) -> \
        Tuple[List[Token], Node]:
        if not node:
            tokens, node = self.int_tag(tokens)
        token: Token = tokens[0]
        if (token.value == '*') | (token.value == '/'):
            tokens = self.advance(tokens, '*', '/')
            tokens, right = self.int_tag(tokens)
            node = Operation(node, Operator(token.value), right)
        else:
            return tokens, node
        # Calls itself recursively to find consecutive operations
        return self.mul_div(tokens, node)
        
    """
    plu_min :: [Token] -> Node -> ([Token], Node)

    When this function is called, it checks if a plus or minus operator can be
    found. If not, continue to call the function mul_div.
    """
    def plu_min(self, tokens: List[Token], node: Optional[Node] = None) -> \
        Tuple[List[Token], Node]:
        if not node:
            tokens, node = self.mul_div(tokens)
        token: Token = tokens[0]
        if (token.value == '+') | (token.value == '-'):
            tokens = self.advance(tokens, '+', '-')
            tokens, right = self.mul_div(tokens)
            node = Operation(node, Operator(token.value), right)
        else:
            return tokens, node
        # Calls itself recursively to find consecutive operations
        return self.plu_min(tokens, node)

    """
    compare :: [Token] -> ([Token], Node)

    When this function is called, it checks if a boolean comparison operator can
    be found, after checking if another expression exists before the operator.
    """
    def compare(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        tokens, node = self.plu_min(tokens)
        token: Token = tokens[0]
        if token.type == 't_COMP':
            tokens = self.advance(tokens, 't_COMP')
            tokens, right = self.plu_min(tokens)
            node = Comparison(node, Operator(token.value), right)
        return tokens, node

    """
    assign :: [Token] -> ([Token], Node)

    When this function is called, it checks if an assignment operator can be
    found, after checking if another expression exists before the operator.
    """
    def assign(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        tokens, node = self.compare(tokens)
        token: Token = tokens[0]
        if token.type == 't_ASSIGN':
            tokens = self.advance(tokens, 't_ASSIGN')
            # Find what's after the assignment operator
            tokens, body = self.begin(tokens)
            node = Assignment(node, body)
        return tokens, node

    """
    print :: [Token] -> ([Token], Node)

    When this function is called, it checks if a print statement can be found.
    If not, continue to call the function assign.
    """
    def print(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        token: Token = tokens[0]
        if token.type == 't_PRINTFUN':
            tokens = self.advance(tokens, 't_PRINTFUN')
            # Collect the body of the print statement
            tokens, body = self.begin(tokens)
            node = Print(body)
            return tokens, node
        return self.assign(tokens)
    
    """
    if_fun :: [Token] -> ([Token], Node)

    When this function is called, it checks if an if statement can be found. If
    not, continue to call the function print.
    """
    def if_fun(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        token: Token = tokens[0]
        if token.type == 't_IFFUN':
            tokens = self.advance(tokens, 't_IFFUN')
            tokens, condition = self.compare(tokens)
            tokens = self.advance(tokens, 't_COLON')
            tokens = self.advance(tokens, 't_ENDOFLINE')
            # Collect the body of the If function, which will be stored in a
            # new root node using the group function
            tokens, body = self.group(tokens, [])
            node = If(condition, body)
            return tokens, node
        return self.print(tokens)

    """
    while_fun :: [Token] -> ([Token], Node)

    When this function is called, it checks if a while function can be found. If
    not, continue to call the function if_fun.
    """
    def while_fun(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        token: Token = tokens[0]
        if token.type == 't_WHILEFUN':
            tokens = self.advance(tokens, 't_WHILEFUN')
            tokens, condition = self.compare(tokens)
            tokens = self.advance(tokens, 't_COLON')
            tokens = self.advance(tokens, 't_ENDOFLINE')
            # Collect the body of the While function, which will be stored in a
            # new root node using the group function
            tokens, body = self.group(tokens, [])
            node = While(condition, body)
            return tokens, node
        return self.if_fun(tokens)

    """
    param_fun :: [Token] -> ([Token], Node)

    When this function is called, it checks if a function can be found. If not,
    continue to call the function while_fun.
    """
    def param_fun(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        token: Token = tokens[0]
        if token.type == 't_PARAMFUN':
            tokens = self.advance(tokens, 't_PARAMFUN')
            tokens, param = self.collect_param(tokens, [])
            tokens = self.advance(tokens, 't_COLON')
            tokens = self.advance(tokens, 't_ENDOFLINE')
            # Collect the body of the new function, which will be stored in a
            # new root node using the group function
            tokens, body = self.group(tokens, [])
            # Return a Function Decleration node, which in turn will return a
            # Function node when called by the Evaluator
            node = FunDec(body, param)
            return tokens, node
        return self.while_fun(tokens)
    
    """
    run :: [Token] -> ([Token], Node)

    When this function is called, it checks if a function call can be found,
    recognized by the 'run' statement. If not, continue to call the function
    param_fun.
    """
    def run(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        token: Token = tokens[0]
        if token.type == 't_RUN':
            tokens = self.advance(tokens, 't_RUN')
            tokens, name = self.int_tag(tokens)
            tokens, param = self.collect_param(tokens, [])
            node = Run(name, param)
            return tokens, node
        return self.param_fun(tokens)
    
    """
    fun_return :: [Token] -> ([Token], Node)

    When this function is called, it checks if a function return statement can
    be found. If not, continue to call the function run.
    """
    def fun_return(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        token: Token = tokens[0]
        if token.type == 't_RETURN':
            tokens = self.advance(tokens, 't_RETURN')
            tokens, body = self.begin(tokens)
            node = Return(body)
            return tokens, node
        return self.run(tokens)

    """
    begin :: [Token] -> ([Token], Node)

    This function is called at the start of the parsing process. It calls the
    function that has the highest precedence.
    """
    def begin(self, tokens: List[Token]) -> Tuple[List[Token], Node]:
        return self.fun_return(tokens)

    """
    collect_param :: [Token] -> [Node] -> ([Token], Node)

    This function is called when a function is declared or called in the code.
    It checks for and returns parameters given to a function decleration or
    call.
    """
    def collect_param(self, tokens: List[Token], nodes: List[Node] = []) -> \
        Optional[Tuple[List[Token], Node]]:
        token: Token = tokens[0]
        if(token.type in ('t_ENDOFLINE', 't_EOF', 't_COLON')):
            return tokens, nodes
        # Parameters are preceded by a '>' character
        if(token.value == '>'):
            tokens = self.advance(tokens, '>')
            tokens, node = self.plu_min(tokens)
            nodes.append(node)
            return self.collect_param(tokens, nodes)
        # If a character is found other than a newline, end of file, colon or
        # '>' character, the code contains an illegal character combination
        self.error()
    
    """
    group :: [Token] -> [Node] -> ([Token], Node)

    This function produces a root Node containing all Nodes within an if, while
    or function declaration. This is necessary to store the body of if, while
    and function statements.
    """
    def group(self, tokens: List[Token], nodes: List[Node] = []) -> \
        Tuple[List[Token], Node]:
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

    """
    log :: [Node] -> Int -> None

    This function is called by the parser at the end of the parsing process to
    log all created nodes to the log file.
    """
    def log(self, nodes: List[Node], pos: int = 0) -> None:
        if pos == 0:
            nodes = list(map((lambda x: str(nodes.index(x)) + '\t' + str(x)), \
                nodes))
        if pos<len(nodes):
            logfile = open("larrylog.txt","a")
            logfile.write('\n' + str(nodes[pos]))
            logfile.close()
            return self.log(nodes, pos+1)
        logfile = open("larrylog.txt","a")
        logfile.write('\n\nLoop and function calls:\t\t\t\t\tWith arguments:')
        logfile.close()

    """
    parse :: [Token] -> [Node] -> [Node]

    This function initially takes the token list and calles itself recursively
    untill all of the tokens are consumed. It calls the begin function to get a
    statement and looks for a new statement when a newline character is found.
    """
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