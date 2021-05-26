import re
from typing import Callable, List, Tuple


class Token(object):
    # __init__ :: String -> String -> None
    def __init__(self, type: str, value: str) -> None:
        self.type: str = type
        self.value: str = value

    # __str__ :: None -> String
    def __str__(self):
        return 'Token[{}, {}]'.format(self.type.__repr__(), self.value.__repr__())

    # __repr__ :: None -> String
    def __repr__(self):
        return self.__str__()


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

    # log :: (String -> [(String, String)] -> Int -> [(String, String)] -> [(String, String)]) -> ([(String, String)] -> Int -> [(String, String)] -> (String -> [(String, String)] -> Int -> [(String, String)] -> [(String, String)]))
    def log(func: Callable) -> Callable:
        # inner :: [(String, String)] -> Int -> [(String, String)] -> (String -> [(String, String)] -> Int -> [(String, String)] -> [(String, String)])
        def inner(*args):
            if(len(args)>3):
                logfile = open("larrylog.txt","a")
                token = str(args[-1][-1])
                logfile.write('\n' + token)
                if(args[3]>=len(args[1])):
                    logfile.write('\nEOF Token\n\n#\tAST Nodes returned by Parser:')
                logfile.close()
            return func(*args)
        return inner

    # lex :: String -> [(String, String)] -> Int -> [(String, String)] -> [(String, String)]
    @log
    def lex(self, characters : str, \
                  exprs : List[Tuple[str, str]], \
                  position : int = 0, \
                  tokens : List[Tuple[str, str]] = []) -> List[Tuple[str, str]]:
        if position >= len(characters):     # base case
            tokens = list(filter((lambda x: x.type != 't_SPACE'), tokens))            # Remove unnecessary SPACE tokens
            tokens.append(Token('t_EOF', None))
            return tokens
        l = self.match_expr(exprs, characters, position)
        position = l[0]
        if len(l) > 1:
            tokens.append(l[1])
        return self.lex(characters, exprs, position, tokens)

    # match_expr :: [(String, String)] -> String -> [Int, (String, String)]
    def match_expr(self, exprs : List[Tuple[str, str]], \
                         characters : str, \
                         position : int) -> Tuple[int, Tuple[str, str]]:
        if len(exprs) == 0:
            self.error('Unknown character {} at {}'.format(characters[position], position))
        match = None
        (pattern, type), *tail = exprs
        regex = re.compile(pattern)
        match = regex.match(characters, position)
        if match:
            l: list = []
            l.append(match.end(0))
            if type:
                value = match.group(0)
                l.append(Token(type, value))
            return l
        return self.match_expr(tail, characters, position)