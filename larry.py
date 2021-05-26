from Lexer import Lexer
from Parser import Parser
from Evaluator import Evaluator
import sys, Expressions

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
tokens = lexer.lex(characters, Expressions.regularExpressions)

parser = Parser()
nodes = parser.parse(tokens)

evaluator = Evaluator()
evaluator.evaluate(nodes)