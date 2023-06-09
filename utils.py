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

def check_for_comment_end(input_string):
    if re.sub(re.compile(r'\s+'),'',input_string)[-2:] == "*/":
        return [token("comment", "multi-end")]
    else:
        return []



def lex(input_string, is_comment_start_found):
    tokens = []
    curr_index = 0
    input_string = input_string.strip()
    if is_comment_start_found:
        return check_for_comment_end(input_string)

    while curr_index < len(input_string):
        curr_char = input_string[curr_index]
        if curr_char.isspace():
            curr_index += 1
        elif curr_char == "#" and curr_index == 0:
            tokens.append(token("comment", "line"))
            return tokens
        elif curr_char == "/" and curr_index == 0 and re.sub(re.compile(r'\s+'),'',input_string)[0:2] == "/*":
            tokens.append(token("comment", "multi-start"))
            return tokens
        elif curr_char.isalpha():
            variable = ""
            start_index = curr_index
            while curr_index < len(input_string) and (input_string[curr_index].isalnum() or input_string[curr_index] == "_"):
                variable += input_string[curr_index]
                curr_index += 1
            if variable.lower() in ["true", "false"]:
                tokens.append(token("kw", variable.lower()))
            else:
                if start_index == 0 and curr_index < len(input_string) and input_string[curr_index] == " " and variable == "print":
                    tokens.append(token("print",variable))
                    curr_index += 1
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
        elif curr_char in ('+', '-', '*', '/', '%', '^') and curr_index+1 < len(input_string) and input_string[curr_index+1] == "=":
            tokens.append(token("ext1", curr_char))
            curr_index += 2
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
                raise_parse_error()
        elif curr_char == "/":
            tokens.append(token("sym","/"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == "%":
            tokens.append(token("sym","%"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == "^":
            tokens.append(token("sym","^"))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == "=":
            curr_index += 1
            if input_string[curr_index] == "=":
                    tokens.append(token("sym","=="))
                    curr_index += 1
            else: tokens.append(token("sym","="))
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == "(":
            tokens.append(token("sym","("))
            curr_index += 1
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == ")":
            tokens.append(token("sym",")"))
            curr_index += 1
            if curr_index == 1:
                raise_parse_error()
        elif curr_char == ">":
            curr_index += 1
            if input_string[curr_index] == "=":
                    tokens.append(token("sym",">="))
                    curr_index += 1
            else: tokens.append(token("sym",">"))
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == "<":
            curr_index += 1
            if input_string[curr_index] == "=":
                    tokens.append(token("sym","<="))
                    curr_index += 1
            else: tokens.append(token("sym","<"))
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == ",":
            tokens.append(token("comma",","))
            curr_index += 1
        elif curr_index + 1 < len(input_string) and input_string[curr_index:curr_index+2] == "||":
            if curr_index + 2 < len(input_string) and input_string[curr_index+2:curr_index+3] =='=':
                tokens.append(token("ext1", '||'))
                curr_index += 3
            else:
                tokens.append(token("sym","||"))
                curr_index += 2
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_char == "!":
            curr_index += 1
            if input_string[curr_index] == "=":
                    tokens.append(token("sym","!="))
                    curr_index += 1
            else: tokens.append(token("sym","!"))
            if curr_index >= len(input_string):
                raise_parse_error()
        elif curr_index + 1< len(input_string) and input_string[curr_index:curr_index+2] == "&&":
            if curr_index + 2 < len(input_string) and input_string[curr_index+2:curr_index+3] =='=':
                tokens.append(token("ext1", '&&'))
                curr_index += 3
            else:
                tokens.append(token("sym","&&"))
                curr_index += 2
            if curr_index >= len(input_string):
                raise_parse_error()
        else:
            raise_parse_error()
    return tokens
        
def parse(statements):
    parsed_statements = []
    is_comment_start_found = False
    for line , statement in enumerate(statements):
        tokens = lex(statement, is_comment_start_found)
        if len(tokens) and tokens[0].typ == "print" and tokens[0].val == "print":
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
        elif len(tokens) and tokens[0].typ == "comment":
            if tokens[0].val == "multi-start":
                is_comment_start_found = True
            elif tokens[0].val == "multi-end" and not is_comment_start_found:
                raise_parse_error()
            elif tokens[0].val == "multi-end":
                is_comment_start_found = False
        elif len(tokens) >= 2 and tokens[0].typ == "var" and tokens[1].typ == "sym" and tokens[1].val == "=":
            if len(tokens) > 2:
                variable_name = tokens[0]
                parsed_statements.append(AssignmentStatement(line , variable_name, infix_to_postfix(tokens))) 
            else:
                raise_parse_error()
        elif len(tokens) > 0:
            parsed_statements.append(ExpressionStatement(line, infix_to_postfix(tokens)))
    if is_comment_start_found:
        raise_parse_error()
    return parsed_statements


def parse_program(lines):
    parsed_statements = []
    parsed_statements = parse(lines)
    # for statement in parsed_statements:
    #    print(statement)
    return parsed_statements

def evaluate_program(statements):
    variables_map = {}
    results = []
    zero_by_division_error_occurred = False
    for statement in statements:
        if isinstance(statement, PrintStatement):
            expressions = statement.expressions
            output = []
            for expression in expressions:
                try:
                    result , variables_map = evaluate_expression(expression, variables_map)
                    if not zero_by_division_error_occurred:
                        output.append(result)
                except ZeroDivisionError:
                    if not zero_by_division_error_occurred:
                        result = "divide by zero"
                        output.append(result)
                    zero_by_division_error_occurred = True
            results.append(output)
        else:
            try:
                result, variables_map = evaluate_expression(statement.expression, variables_map)
            except ZeroDivisionError:
                if not zero_by_division_error_occurred:
                    results.append(["divide by zero"])
                zero_by_division_error_occurred = True
    print_program_result(results)
    return


def print_program_result(results):
    for item in results:
        if len(item) > 0:
            print(*item, sep = ' ')     
    return          
                

def raise_parse_error():
  print("parse error")
  sys.exit(0)             

def handle_unary_negation(tokens, operators):
    for i, curr_token in enumerate(tokens):
        if curr_token.typ == "sym" and curr_token.val == "-":
            if i == 0 or tokens[i-1].val == "(" or (tokens[i-1].val in operators and tokens[i-1].val not in ["++","--"]):
                tokens[i] = token("sym", "unary-")
    return tokens

def handle_ext1(tokens, operators):
    i = 0
    while i < len(tokens):
        curr_token = tokens[i]
        if curr_token.typ == "ext1" :
            if i == 0 or tokens[i-1].typ != "var":
                raise_parse_error() 
            tokens[i] = token("sym","=")
            tokens.insert(i +  1, tokens[i-1])
            tokens.insert(i + 2, token("sym", curr_token.val))
            i += 3
        else:
            i += 1
    return tokens


def infix_to_postfix(tokens) :
    operators = {
        '=': (1, 'right'),
        '+': (3, 'left'), 
        '-': (3, 'left'), 
        '&&': (3, 'left'),
        '||': (3, 'left'),
        '*': (4, 'left'), 
        '/': (4, 'left'), 
        '%': (4, 'left'), 
        '^': (5, 'right'), 
        'unary-': (6, 'non'), 
        '++': (7, 'non'), 
        '--': (7, 'non'),
        '==': (3, 'non'),
        '!': (6, 'non'),
        '!=': (6, 'non'),
        '>': (2, 'left'),
        '>=': (2, 'left'),
        '<': (2, 'left'),
        '<=': (2, 'left'),
    }
    tokens = handle_unary_negation(tokens, operators)
    tokens = handle_ext1(tokens, operators)
    postfix = []
    operator_stack = []
    last_token = None
    for i, curr_token in enumerate(tokens):
        if curr_token.typ == "val":
            curr_token.val = float(curr_token.val)
            postfix.append(curr_token)
        elif curr_token.typ == "kw":
            if curr_token.val == "true":
                operator_stack.append(token("val",float(1)))
            else:
                operator_stack.append(token("val",float(0)))
        elif curr_token.typ == "var":
            if last_token and last_token.val in ["++" , "--"]:
                inc_dec = postfix[-1] 
                postfix[-1] = curr_token
                postfix.append(token("PRE",inc_dec.val))
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
        elif curr_token.typ == "sym" and curr_token.val in ['++',  '--']:
            if curr_token.val in ['++', '--']:
                if not((last_token and last_token.typ == "var") or (i + 1 < len(tokens) and tokens[i + 1].typ == "var")):
                    raise_parse_error()
                postfix.append(token('POST', curr_token.val))
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

def evaluate_expression(expression, variables_map):
    operator_stack = []
    # print(expression)
    for i, curr_token in enumerate(expression):
        # print(curr_token, operator_stack)
        if curr_token.typ == "val":
            operator_stack.append(curr_token)
        elif curr_token.typ == "var":
            if curr_token.val not in variables_map:
                variables_map[curr_token.val] = float(0.0)
            if (i + 1 <= len(expression) and expression[-1-i].val == "=") or (i +1<len(expression) and expression[i+1].typ in ("POST" ,"PRE")):
                operator_stack.append(curr_token)
            else:
                operator_stack.append(token("val",variables_map[curr_token.val]))
        elif curr_token.val in ('+', '-', '*', '/', '%', '^', '||', '&&', '==', '!=', '>', '<', '>=', '<='):
            if len(operator_stack) < 2:
                raise_parse_error()
            right_operand = operator_stack.pop()
            left_operand = operator_stack.pop()
            result = evaluate_binary_operation(left_operand, right_operand, curr_token,variables_map)
            operator_stack.append(token("val",result))
        elif curr_token.val in ("unary-", '!'):
            if len(operator_stack) < 1:
                raise_parse_error()
            operand = operator_stack.pop()
            result = evaluate_unary_operation(operand, curr_token, variables_map)
            operator_stack.append(token("val",result))
        elif curr_token.val in ('++', '--'):
            if len(operator_stack) < 1 or operator_stack[-1].typ != "var":
                raise_parse_error()
            operand = operator_stack.pop()
            result = evaluate_unary_operation(operand, curr_token,variables_map)
            if curr_token.typ == "POST":
                operator_stack.append(token("val",variables_map[operand.val]))
            else:
                operator_stack.append(token("val",result))
            variables_map[operand.val] = result
        elif curr_token.val == '=':
            if len(operator_stack) < 2:
                raise_parse_error()
            right_operand = operator_stack.pop()
            left_operand = operator_stack.pop()
            if left_operand.typ != "var":
                raise_parse_error()
            if right_operand.typ == "var":
                variables_map[left_operand.val] = variables_map[right_operand.val]
            else:
                variables_map[left_operand.val] = right_operand.val                
            operator_stack.append(right_operand)
        else:
            raise_parse_error()
    if len(operator_stack) != 1:
        raise_parse_error()
    if operator_stack[0].typ == "var":
        return variables_map.get(operator_stack[0].val, float(0.0)), variables_map
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
            raise ZeroDivisionError()
        return left_value / right_value
    elif operator.val == '%':
        if right_value == 0:
            raise ZeroDivisionError()
        return left_value % right_value
    elif operator.val == '^':
        return pow(left_value, right_value)
    elif operator.val == '||':
        return int(bool(left_value) or bool(right_value))
    elif operator.val == '&&':
        return int(bool(left_value) and bool(right_value))
    elif operator.val == '>':
        return int(left_value > right_value)
    elif operator.val == '>=':
        return int(left_value >= right_value)
    elif operator.val == '<':
        return int(left_value < right_value)
    elif operator.val == '<=':
        return int(left_value <= right_value)
    elif operator.val == '==':
        return int(left_value == right_value)
    elif operator.val == '!=':
        return int(not bool(left_value == right_value))


def evaluate_unary_operation(operand, operator,variables_map) -> float:
    value = operand.val
    if operand.typ == "var":
      value = variables_map[operand.val]
    if operator.val == '++':
        return value + float(1.0)
    elif operator.val == '--':
        return value - float(1.0)
    elif operator.val == 'unary-':
        return (-1)* value
    elif operator.val == '!':
        return int(not bool(value))
    
