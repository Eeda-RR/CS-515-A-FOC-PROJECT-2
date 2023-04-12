import sys
import re

class token():
    typ: str
    val: str
    def __init__(self, typ, val):
        """
        >>> token('sym', '(')
        token('sym', '(')
        """
        self.typ = typ
        self.val = val

    def __repr__(self):
        return f'token({self.typ!r}, {self.val!r})'

class Statement():
    def __init__(self, _type, line):
        self.type = _type
        self.line = line

class PrintStatement(Statement):
    def __init__(self, line, expressions):
        Statement.__init__(self,"PRINT", line)
        self.expressions = expressions
    def __repr__(self):
        return f'PrintStatement(Expression: {self.expressions!r})'

class AssignmentStatement(Statement):
    def __init__(self, line, variable_name, expression):
        Statement.__init__(self,"ASSIGNMENT", line)
        self.variable_name = variable_name
        self.expression = expression
    
    def __repr__(self):
        return f'AssignmentStatement(Variable: {self.variable_name!r}, Expression: {self.expression!r}'

class ExpressionStatement(Statement):
    def __init__(self, line, expression):
        Statement.__init__(self,"EXPRESSION", line)
        self.expression = expression
    
    def __repr__(self):
        return f'ExpressionStatement({self.expression!r})'



def lex(input_string):
    tokens = []
    curr_index = 0
    while curr_index < len(input_string):
        curr_char = input_string[curr_index]
        if curr_char.isspace():
            curr_index += 1
        elif curr_char.isalpha():
            variable = ""
            while curr_index < len(input_string) and (input_string[curr_index].isalnum() or input_string[curr_index] == "_"):
                variable += input_string[curr_index]
                curr_index += 1
            if variable in ["true", "false"]:
                tokens.append(token("kw", variable))
            else:
                tokens.append(token("var",variable))
        elif curr_char.isdigit():
            number = ''
            while curr_index < len(input_string) and (input_string[curr_index].isdigit() or input_string[curr_index] == "."):
                number += input_string[curr_index]
                curr_index += 1
            if number[-1] == ".":
                raise_parse_error()
            else:
                tokens.append(token("val",float(number)))
        elif curr_char == "+":
            curr_index += 1
            if curr_index < len(input_string):
                if input_string[curr_index] == "+":
                    tokens.append(token("sym","++"))
                    curr_index += 1
                else:
                    tokens.append(token("sym","+"))
            else:
                raise_parse_error()
        elif curr_char == "-":
            curr_index += 1
            if curr_index < len(input_string):
                if input_string[curr_index] == "-":
                    tokens.append(token("sym","--"))
                    curr_index += 1
                else:
                    tokens.append(token("sym","-"))
            else:
                raise_parse_error()
        elif curr_char == "*":
            tokens.append(token("sym","*"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "/":
            tokens.append(token("sym","/"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "%":
            tokens.append(token("sym","%"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "^":
            tokens.append(token("sym","^"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "=":
            tokens.append(token("sym","="))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "(":
            tokens.append(token("sym","("))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == ")":
            tokens.append(token("sym",")"))
            curr_index += 1
            if curr_index == 1:
                raise_parse_error
        elif curr_char == ",":
            tokens.append(token("comma",","))
            curr_index += 1
        elif curr_index + 1 < len(input_string) and input_string[curr_index:curr_index+2] == "||":
            tokens.append(token("sym","||"))
            curr_index += 2
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_char == "!":
            tokens.append(token("sym","!"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error
        elif curr_index + 1< len(input_string) and input_string[curr_index:curr_index+2] == "&&":
            tokens.append(token("sym","&&"))
            curr_index += 2
            if curr_index >= len(input_string):
                raise_parse_error
        else:
            raise_parse_error()
    return tokens
        
def parse(statements):
    parsed_statements = []
    for line , statement in enumerate(statements):
        tokens = lex(statement)
        if len(tokens) and tokens[0].typ == "var" and tokens[0].val == "print":
            expressions = []
            index = 1
            expression = []
            while index < len(tokens):
                if tokens[index].typ != "comma":
                    expression.append(tokens[index])
                else:
                    expressions.append(infix_to_postfix(expression))
                    expression = []
                index += 1
            if len(expression) > 0:
                expressions.append(infix_to_postfix(expression))
            if len(expressions) == 0:
                raise_parse_error()     
            parsed_statements.append(PrintStatement(line, expressions)) 
        elif len(tokens) >= 2 and tokens[0].typ == "var" and tokens[1].typ == "sym" and tokens[1].val == "=":
            if len(tokens) > 2:
                variable_name = tokens[0]
                parsed_statements.append(AssignmentStatement(line , variable_name, infix_to_postfix(tokens))) 
            else:
                raise_parse_error()
        elif len(tokens) > 0:
            parsed_statements.append(ExpressionStatement(line, infix_to_postfix(tokens)))
    return parsed_statements


def parse_program(lines):
    parsed_statements = []
    parsed_statements = parse(lines)
    # for statement in parsed_statements:
    #    print(statement)
    return parsed_statements

def evaluate_program(statements):
    variables_map = {}
    for statement in statements:
        if isinstance(statement, PrintStatement):
            expressions = statement.expressions
            output = []
            try:
                for expression in expressions:
                    result , variables_map = evaluate_expression(expression, variables_map)
                    output.append(result)
            except ZeroDivisionError:
                output.append("divide by zero")
            print(*output, sep=" ")
        else:
            try:
                result, variables_map = evaluate_expression(statement.expression, variables_map)
            except ZeroDivisionError:
                print("divide by zero")
                

def raise_parse_error():
  print("parse error")
  sys.exit(1)             


def infix_to_postfix(tokens) :
    operators = {
        '=': (1, 'right'),
        '+': (2, 'left'), 
        '-': (2, 'left'), 
        '*': (3, 'left'), 
        '/': (3, 'left'), 
        '%': (3, 'left'), 
        '^': (4, 'right'), 
        'unary-': (5, 'non'), 
        '++': (5, 'non'), 
        '--': (5, 'non'),
        '~': (5, 'non')
    }
    postfix = []
    operator_stack = []
    last_token = None
    for i, curr_token in enumerate(tokens):
        if curr_token.typ == "val":
            curr_token.val = float(curr_token.val)
            postfix.append(curr_token)
        elif curr_token.typ == "var":
            if last_token and last_token.val in ["++" , "--"]:
                postfix[-1] = token("pre"+last_token.val,curr_token)
            else:
                postfix.append(curr_token)
        elif curr_token.typ == "sym" and curr_token.val == "(":
            operator_stack.append(curr_token)
        elif curr_token.typ == "sym" and curr_token.val == ")":
            while operator_stack and operator_stack[-1].val != '(':
                postfix.append(operator_stack.pop())
            if not operator_stack:
                raise_parse_error()
            operator_stack.pop()
        elif curr_token.typ == "sym" and curr_token.val == '=':
            while operator_stack and operator_stack[-1].val != '(':
                postfix.append(operator_stack.pop())
            operator_stack.append(curr_token)
        elif curr_token.typ == "sym" and curr_token.val in ['++',  '--']:
            if curr_token.val in ['++', '--']:
                if (last_token and last_token.typ == "var") or (i + 1 < len(tokens) and tokens[i].typ == "var")
                    raise_parse_error()
                postfix.append(curr_token)
            else:
                while operator_stack and operator_stack[-1].val != '(' and operators[curr_token.val][0] < operators[operator_stack[-1].val][0]:
                    postfix.append(operator_stack.pop())
                    if operator_stack and operator_stack[-1].val != '(' and operators[curr_token.val][0] == operators[operator_stack[-1].val][0]:
                        if operators[curr_token.val][1] == 'left':
                            postfix.append(operator_stack.pop())
                operator_stack.append(curr_token)
        elif curr_token.val in operators:
            prec, associativity = operators[curr_token.val]
            while operator_stack and operator_stack[-1].val != '(':
                top_token = operator_stack[-1]
                if top_token.val not in operators:
                    break
                top_prec, top_associativity = operators[top_token.val]
                if (associativity == 'left' and prec <= top_prec) or (associativity == 'right' and prec < top_prec):
                    postfix.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(curr_token)
            if i == len(tokens) - 1:
                raise_parse_error()
        last_token = curr_token
    while operator_stack:
        operator = operator_stack.pop()
        if operator == '(':
            raise_parse_error()
        postfix.append(operator)
    return postfix

def evaluate_expression(expression, variables_map) :
    operator_stack = []
    for i, curr_token in enumerate(expression):
        if curr_token.typ == "val":
            operator_stack.append(curr_token)
        elif curr_token.typ == "var":
            if curr_token.val not in variables_map:
              variables_map[curr_token.val] = float(0.0)
            operator_stack.append(curr_token)
        elif curr_token.val in ('+', '-', '*', '/', '%', '^'):
            right_operand = operator_stack.pop()
            left_operand = operator_stack.pop()
            result = evaluate_binary_operation(left_operand, right_operand, curr_token,variables_map)
            operator_stack.append(token("val",result))

        elif curr_token.val in ('++', '--'):
            # if not( is_variable(expression[i-1]) or is_variable(expression[i+1])):
            #     raise ValueError('Operator {} not followed or prefixed by variable'.format(token))
            #post inc/ dec
            operand = operator_stack.pop()
            operator_stack.append(token("val",variables_map[operand.val]))
            result = evaluate_unary_operation(operand, curr_token,variables_map)
            variables_map[operand.val] = result
        elif curr_token.typ in ("pre++", "pre--"):
            operand = curr_token.val
            result = evaluate_unary_operation(operand,token("sym",curr_token.typ[3:]),variables_map)
            operator_stack.append(token("val",result))
            variables_map[operand.val] = result

        elif curr_token.val == '=':
            if len(operator_stack) < 2:
                raise ValueError('Not enough operands for operator {}'.format(curr_token))
            right_operand = operator_stack.pop()
            left_operand = operator_stack.pop()
            if left_operand.typ != "var":
                raise ValueError('Left operand of assignment operator must be a variable')
            variables_map[left_operand.val] = right_operand.val
            operator_stack.append(token("val",right_operand.val))
        else:
            raise ValueError('Invalid token: {}'.format(curr_token))
    if len(operator_stack) != 1:
        raise ValueError('Invalid expression: {}'.format(expression))
    if operator_stack[0].typ == "var":
        return variables_map[operator_stack[0].val], variables_map
    return operator_stack[0].val, variables_map

def evaluate_binary_operation(left_operand, right_operand, operator,variables_map) -> float:
    left_value = left_operand.val
    right_value = right_operand.val
    if left_operand.typ == "var":
      left_value = variables_map[left_operand.val]
    if right_operand.typ == "var":
      right_value = variables_map[right_operand.val]
    if operator.val == '+':
        return left_value + right_value
    elif operator.val == '-':
        return left_value - right_value
    elif operator.val == '*':
        return left_value * right_value
    elif operator.val == '/':
        if right_value == 0:
            raise ZeroDivisionError('Division by zero')
        return left_value / right_value
    elif operator.val == '%':
        if right_value == 0:
            raise ZeroDivisionError('Modulo by zero')
        return left_value % right_value
    elif operator.val == '^':
        return pow(left_value, right_value)


def evaluate_unary_operation(operand, operator,variables_map) -> float:
    value = operand.val
    if operand.typ == "var":
      value = variables_map[operand.val]
    if operator.val == '++':
        return value + 1
    elif operator.val == '--':
        return value - 1
    else:
        raise ValueError('Invalid operator: {}'.format(operator))