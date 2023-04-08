class Parser:
    def __init__(self):
        self.tokens = []
        self.input_string = ""
        self.curr_index = 0
        

    def parse_and_get_tokens(self, input_string):
        self.tokens = []
        self.input_string = input_string
        self.curr_index = 0
        while self.curr_index < len(input_string):
            curr_char = self.input_string[self.curr_index]
            if curr_char == " ":
                self.curr_index += 1
            elif curr_char.isdigit():
                self.tokens.append(("NUMBER", self.get_number()))
            elif curr_char.isalpha():
                self.tokens.append(("VARIABLE", self.get_variable_name()))
            elif curr_char == "+":
                self.curr_index += 1
                if self.curr_index < len(input_string):
                    if self.input_string[self.curr_index] == "+":
                        self.tokens.append(("INC", None))
                        self.curr_index += 1
                    else:
                        self.tokens.append(("PLUS", None))
                else:
                    self.parseError()
            elif curr_char == "-":
                self.curr_index += 1
                if self.curr_index < len(input_string):
                    if self.input_string[self.curr_index] == "-":
                        self.tokens.append(("DEC", None))
                        self.curr_index += 1
                    else:
                        self.tokens.append(("MINUS", None))
                else:
                    self.parseError()
            elif curr_char == "*":
                self.tokens.append(("MULTIPLY", None))
                self.curr_index += 1
            elif curr_char == "/":
                self.tokens.append(("DIVIDE", None))
                self.curr_index += 1
            elif curr_char == "%":
                self.tokens.append(("MOD", None))
                self.curr_index += 1
            elif curr_char == "^":
                self.tokens.append(("EXP", None))
                self.curr_index += 1
            elif curr_char == "=":
                self.tokens.append(("EQ", None))
                self.curr_index += 1
            elif curr_char == "(":
                self.tokens.append(("LPARANTHESIS", None))
                self.curr_index += 1
            elif curr_char == ")":
                self.tokens.append(("LPARANTHESIS", None))
                self.curr_index += 1
            else:
                return self.parseError()
        return self.tokens

    def parseError(self):
        print("parse error")
        return -1
    
    def get_number(self):
        number = float(0)
        float_point_found = False
        factor = 10
        while self.curr_index < len(self.input_string) and (self.input_string[self.curr_index].isdigit() or self.input_string[self.curr_index] == "."):
            if self.input_string[self.curr_index] == ".":
                if float_point_found:
                    return self.parseError()
                else:
                    float_point_found = True
                    factor = factor / 10
                    self.curr_index += 1
            else:
                if float_point_found:
                    factor = factor / 10
                    number = number + (factor* int(self.input_string[self.curr_index]))
                else:
                    number = (number*10) + int(self.input_string[self.curr_index])
                self.curr_index += 1
        return number
    
    def get_variable_name(self):
        variable = ""
        while self.curr_index < len(self.input_string) and (self.input_string[self.curr_index].isalnum() or self.input_string[self.curr_index] == "_"):
            variable += self.input_string[self.curr_index]
            self.curr_index += 1
            if variable == "print" and self.curr_index < len(self.input_string) and self.input_string[self.curr_index] == " ":
                self.curr_index += 1
                self.handle_print()
                return
        return variable
    
    def handle_print(self):
        if self.curr_index < len(self.input_string):
            self.tokens.append(("PRINT", self.input_string[self.curr_index:].split(",")))
        else:
            return self.parseError()




    
            