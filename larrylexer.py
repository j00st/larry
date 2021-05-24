import sys, re
from typing import List, Tuple, Union


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token[%s, %s]' %(self.type, self.value)

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self):
        pass

    def __repr__(self):
        return 'Lexer'

    def error(self, msg = 'unknown error'):
        raise Exception('Lexer error: ' + msg)

    def log(func):
        def inner(*args):
            if(len(args)>3):
                log = open("larrylog.txt","a")
                log.write('\n' + str(args[-1][-1]))
                if(args[3]>=len(args[1])):
                    log.write('\nEOF Token\n')
                log.close()
            return func(*args)
        return inner

    # lex :: String -> [(String, String)] -> Integer -> \
    # [(String, String)] -> Function | [(String, String)]
    @log
    def lex(self, characters : str, \
                  exprs : List[Tuple[str, str]], \
                  position : int = 0, \
                  tokens : List[Tuple[str, str]] = []) -> List[Tuple[str, str]]:
        if position >= len(characters):     # base case
            tokens.append(Token('t_EOF', None))
            return tokens
        l = self.match_expr(exprs, characters, position)
        position = l[0]
        if len(l) > 1:
            tokens.append(l[1])
        return self.lex(characters, exprs, position, tokens)

    # match_expr :: [(String, String)] -> String -> Function | [int, (str, str)]
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
            l = []
            l.append(match.end(0))
            if type:
                value = match.group(0)
                if type == 't_INT' or type == 't_TAG':
                    l.append(Token(type, value))
                elif type == 't_RAW':
                    l.append(Token(type, value[1:-1]))
                elif type == 't_ENDOFLINE':
                    l.append(Token(type, '\\n'))
                else:
                    l.append(Token(type, value))
            return l
        return self.match_expr(tail, characters, position)