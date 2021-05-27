# Larry

Larry is an imperative programming language with an extremely simple syntax. It features the core functionality of any imperative language. It's easily used by experienced programmers and easily learned by inexperienced programmers.

## Installation

Simply clone or download the repository.

## Usage

Larry code can be written with any text editor. For running Larry code, the interpreter is called with Python 3.0 or above.

```python
python larry.py <filename>.larry
```

## Features

Larry supports if and while statements, functions, (double) recursive functions, print statements, most common operations (add, subtract, multiply, divide) and boolean comparison (<,>,<=,>=,==,!=).

Another feature is the log feature. When the interpreter is executed, a logfile will be generated in larrylog.txt in the root folder of Larry.

Errors are returned by the Lexer, Parser and Interpreter to guide you when something goes wrong. Also refer to the larrylog.txt file when errors occur, as it is generated at runtime and can give you an idea of what went wrong.

## Syntax

The various language features are demonstrated in the code in the Examples folder. A list of common features is given below.

```python
# Declare a variable
var = 0

# Declare a function with parameter
f = fun>var:
print var
end

# If statement
if var < 10:
print var
end

# While loop
while var <= 10:
print var
var = var + 1
end
```

## License
[MIT](https://mit-license.org/)