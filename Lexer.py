import re
from typing import Callable, List, Tuple


"""
class Token: For Token objects that will be generated by the Lexer and used by 
the Parser

Token objects consist of a token type and a value. For instance type 't_OPER'
for an operator with value '+'.
"""
class Token(object):
    # __init__ :: String -> String -> None
    def __init__(self, type: str, value: str) -> None:
        self.type: str = type
        self.value: str = value

    # __str__ :: None -> String
    def __str__(self):
        return 'Token[{}, {}]'\
            .format(self.type.__repr__(), self.value.__repr__())

    # __repr__ :: None -> String
    def __repr__(self):
        return self.__str__()


"""
class Lexer: Funcitonality mainly takes characters and produces Token objects

In order to produce Token objects, the Lexer uses Regex to recognize various
patterns in the code.
"""
class Lexer(object):
    # __init__ :: None -> None
    def __init__(self) -> None:
        pass

    # __str__ :: None -> String
    def __str__(self) -> str:
        return 'Lexer'
    
    # __repr__ :: None -> String
    def __repr__(self) -> str:
        return self.__str__()

    # error :: String -> None
    def error(self, msg: str = 'unknown error') -> None:
        raise Exception('Lexer error: ' + msg)

    """
    log :: (String -> [(String, String)] -> Int -> [(String, String)] -> \
           [(String, String)]) -> ([(String, String)] -> Int -> \
           [(String, String)] -> (String -> [(String, String)] -> Int -> \
           [(String, String)] -> [(String, String)]))

    The log function is used as decorator on the lex function. It takes 
    information from the parameter list of lex and logs it to the logfile.
    """
    def log(func: Callable) -> Callable:
        # inner :: [(String, String)] -> Int -> [(String, String)] ->
        #          (String -> [(String, String)] -> Int -> \
        #          [(String, String)] -> [(String, String)])
        def inner(*args):
            # If the function gets three arguments, the token list contains
            # information to log
            if len(args)>3:
                logfile = open("larrylog.txt","a")
                token = str(args[-1][-1])
                logfile.write('\n' + token)
                # When all tokens are logged, end with a manual EOF Token
                if args[3]>=len(args[1]):
                    logfile.write('\nEOF Token\n\n#\tNodes returned by Parser:')
                logfile.close()
            return func(*args)
        return inner

    """
    lex :: String -> [(String, String)] -> Int -> [(String, String)] -> \
           [(String, String)]
    
    The lex function takes the larry code and returns a token list. It utilizes
    the match_expr function to generate Token objects.
    """
    @log
    def lex(self, characters : str, exprs : List[Tuple[str, str]], \
                  position : int = 0, \
                  tokens : List[Tuple[str, str]] = []) -> List[Tuple[str, str]]:
        # Base case
        if position >= len(characters):
            # Remove unnecessary SPACE tokens
            tokens = list(filter((lambda x: x.type != 't_SPACE'), tokens))
            tokens.append(Token('t_EOF', None))
            return tokens
        # lexed contains the current position in the code followed by the
        # returned token object
        lexed = self.match_expr(exprs, characters, position)
        position = lexed[0]
        if len(lexed) > 1:
            tokens.append(lexed[1])
        return self.lex(characters, exprs, position, tokens)

    """
    match_expr :: [(String, String)] -> String -> [Int, (String, String)]

    This function takes the code and the current position and returns what
    token can be found at that position. For this it uses regex. The regular
    expressions stored in a seperate file are matched to the code at the
    current position.
    """
    def match_expr(self, exprs : List[Tuple[str, str]], \
                         characters : str, \
                         position : int) -> List[Tuple[int, Tuple[str, str]]]:
        # If all regular expressions are checked but the function is still
        # called (recursively), the code contains text that cannot be recognized
        if len(exprs) == 0:
            self.error('Unknown character {} at {}'\
                .format(characters[position], position))
        match = None
        (pattern, type), *tail = exprs
        regex = re.compile(pattern)
        match = regex.match(characters, position)
        # If a match is found, return a list containing the new position in the
        # code and a generated Token object
        if match:
            lexed: list = []
            lexed.append(match.end(0))
            if type:
                value = match.group(0)
                lexed.append(Token(type, value))
            return lexed
        return self.match_expr(tail, characters, position)