class Token:
    def __init__(self, token_type, value, line):
        self.type = token_type
        self.value = value
        self.line = line

    def __str__(self):
        return "\nType : " + self.type + "Value: " + str(value)

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
