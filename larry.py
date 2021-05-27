from Lexer import Lexer
from Parser import Parser
from Evaluator import Evaluator
import sys, Expressions

# Read the file to interpret from the command line
if len(sys.argv) != 2:
    sys.stderr.write('Please mention a larry file\n')
    sys.exit(1)
filename = sys.argv[1]

# Create or open logfile. Writing mode clears potential existing logs.
logfile = open("larrylog.txt","w")
logfile.write("Log of program {}\n\nTokens returned by Lexer:".format(filename))
logfile.close()

# Open the larry code file
file = open(filename)
characters = file.read()
file.close()

# Instantiate a Lexer; lex the code into tokens
lexer = Lexer()
tokens = lexer.lex(characters, Expressions.regularExpressions)

# Instantiate a Parser, parse the tokens into nodes
parser = Parser()
nodes = parser.parse(tokens)

# Instantiate an Evaluator, evaluate the nodes
evaluator = Evaluator()
evaluator.evaluate(nodes)