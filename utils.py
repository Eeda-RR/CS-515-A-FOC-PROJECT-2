import sys
import re

class Statement():
    def __init__(self, _type, line):
        self.type = _type
        self.line = line

class PrintStatement(Statement):
    def __init__(self, line, expressions):
        Statement.__init__(self,"PRINT", line)
        self.expressions = expressions
    def __str__(self):
        return "\nPrintStatement: Expression : " + str(self.expressions)


class AssignmentStatement(Statement):
    def __init__(self, line, variable_name, expression):
        Statement.__init__(self,"ASSIGNMENT", line)
        self.variable_name = variable_name
        self.expression = expression
    
    def __str__(self):
        return "\nAssignmentStatement: Variable: " + self.variable_name + " Expression: " + str(self.expression)

class ExpressionStatement(Statement):
    def __init__(self, line, expression):
        Statement.__init__(self,"EXPRESSION", line)
        self.expression = expression
    
    def __str__(self):
        return "\nExpressionStatement : " + str(self.expression)


def get_statement_tokens(input_string):
    tokens = []
    curr_index = 0
    while curr_index < len(input_string):
        curr_char = input_string[curr_index]
        if curr_char == " ":
            curr_index += 1
        elif curr_char.isalpha():
            variable_name = ""
            while curr_index < len(input_string) and (input_string[curr_index].isalnum() or input_string[curr_index] == "_"):
                variable_name += input_string[curr_index]
                curr_index += 1
            tokens.append(variable_name)
        elif curr_char.isdigit():
            number = ''
            while curr_index < len(input_string) and (input_string[curr_index].isdigit() or input_string[curr_index] == "."):
                number += input_string[curr_index]
                curr_index += 1
            if number[-1] == ".":
                raise_parse_error()
            else:
                tokens.append(float(number))
        elif curr_char == "+":
            curr_index += 1
            if curr_index < len(input_string):
                if input_string[curr_index] == "+":
                    tokens.append("++")
                    curr_index += 1
                else:
                    tokens.append("+")
            else:
                raise_parse_error()
        elif curr_char == "-":
            curr_index += 1
            if curr_index < len(input_string):
                if input_string[curr_index] == "-":
                    tokens.append("--")
                    curr_index += 1
                else:
                    tokens.append("-")
            else:
                raise_parse_error()
        elif curr_char == "*":
            tokens.append("*")
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "/":
            tokens.append("/")
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "%":
            tokens.append("%")
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "^":
            tokens.append("^")
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "=":
            tokens.append("=")
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "(":
            tokens.append("(")
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == ")":
            tokens.append(")")
            curr_index += 1
            if curr_index == 1:
                raise_parse_error
        elif curr_char == ",":
            tokens.append(",")
            curr_index += 1
        else:
            raise_parse_error()
    return tokens
        



def get_parsed_statements(statements):
    parsed_statements = []
    for line , statement in enumerate(statements):
        # remove white spaces
        statement = re.sub(re.compile(r'\s+'), ' ', statement)      
        # remove trailing and leading spaces
        statement = statement.strip()
        tokens = get_statement_tokens(statement)
        if len(tokens) and tokens[0] == "print":
            expressions = []
            index = 1
            expression = []
            while index < len(tokens):
                if tokens[index] != ",":
                    expression.append(tokens[index])
                else:
                    expressions.append(expression)
                    expression = []
            if len(expression) > 0:
                expressions.append(expression)
            if len(expressions) == 0:
                raise_parse_error()     
            parsed_statements.append(PrintStatement(line, expressions)) 
        elif len(tokens) >= 2 and is_variable(tokens[0]) and tokens[1] == "=":
            if len(tokens) > 2:
                variable_name = tokens[0]
                parsed_statements.append(AssignmentStatement(line , variable_name, tokens[2:])) 
            else:
                raise_parse_error()
        elif len(tokens) > 0:
            parsed_statements.append(ExpressionStatement(line, tokens))
    return parsed_statements
                    

def is_variable(input):
  pattern = re.compile("[a-zA-Z][a-zA-Z0-9_]*")
  return True if pattern.match(input) else False

def is_number(input):
  pattern = re.compile("\d+(\.\d*)?")
  return True if pattern.match(input) else False

def raise_parse_error():
  print("parse error")
  sys.exit(1)             

