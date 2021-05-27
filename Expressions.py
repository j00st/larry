from typing import List, Tuple

# The RegularExpressions list contains the expressions used by the match_exprs
# function in ./Lexer.py
regularExpressions: List[Tuple[str, str]] = [
    (r'end',                       't_ENDFUN'),
    (r'\n+',                       't_ENDOFLINE'),
    (r'print\s',                   't_PRINTFUN'),
    (r'if\s',                      't_IFFUN'),
    (r'while\s',                   't_WHILEFUN'),
    (r'fun',                       't_PARAMFUN'),
    (r'run\s',                     't_RUN'),
    (r'return\s',                  't_RETURN'),
    (r'[0-9]+',                    't_INT'),
    (r'[A-Za-z][A-Za-z0-9_]*',     't_TAG'),
    (r'<=',                        't_COMP'),
    (r'<',                         't_COMP'),
    (r'>=',                        't_COMP'),
    (r'>',                         't_COMP'),
    (r'!=',                        't_COMP'),
    (r'==',                        't_COMP'),
    (r'\=',                        't_ASSIGN'),
    (r'\(',                        't_LPAR'),
    (r'\)',                        't_RPAR'),
    (r'\{',                        't_LBRA'),
    (r'\}',                        't_RBRA'),
    (r':',                         't_COLON'),
    (r'\+',                        't_OPER'),
    (r'-',                         't_OPER'),
    (r'\*',                        't_OPER'),
    (r'/',                         't_OPER'),
    (r'\s',                        't_SPACE')
]