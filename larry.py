from larrylexer import Lexer
from larryparser import Parser
from larryevaluator import Evaluator
import sys, larryexpressions


if len(sys.argv) != 2:
    sys.stderr.write('Please mention a file to lex\n')
    sys.exit(1)
filename = sys.argv[1]
file = open(filename)
characters = file.read()
file.close()
lexer = Lexer()
tokens = lexer.lex(characters, larryexpressions.regularExpressions)

print('=== TOKENS ===')
for token in tokens:
    print(token)

parser = Parser(tokens)
nodes = parser.parse()

print('=== NODES ===')
for node in nodes:
    print(node)

print('=== OUTPUT ===')

evaluator = Evaluator()
evaluator.evaluate(nodes)

print('=== MEMORY ===')
print(evaluator.globalmemory)