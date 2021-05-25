from larrylexer import Lexer
from larryparser import Parser
from larryevaluator import Evaluator
import sys, larryexpressions

if len(sys.argv) != 2:
    sys.stderr.write('Please mention a larry file\n')
    sys.exit(1)
filename = sys.argv[1]

logfile = open("larrylog.txt","w")
logfile.write("Log of program {}\n\nTokens returned by Lexer:".format(filename))
logfile.close()

file = open(filename)
characters = file.read()
file.close()
lexer = Lexer()
tokens = lexer.lex(characters, larryexpressions.regularExpressions)
parser = Parser(tokens)
nodes = parser.parse()
evaluator = Evaluator()
evaluator.evaluate(nodes)