import re
import Parser

def top_level_parser():
    lines = []
    while True:
        user_input = input()
        # if user pressed Enter without a value, break out of loop
        if user_input == '':
            break
        else:
            user_input = remove_spaces(user_input)
            lines.append(user_input)
    return lines

def remove_spaces(input_str):
    # remove white spaces
    pattern = re.compile(r'\s+')
    input_str = re.sub(pattern, ' ', input_str)
    # remove leading and trailing spaces
    input_str.strip()
    # input_str.split(" ")
    return input_str
   
    




def main():
    result = 1
    while result != -1:
        user_input = top_level_parser()
        parser = Parser()
        statements = []
        for line in user_input:
            statement.append(parser.parse_and_get_tokens(item))
            
    print(res)


if __name__=="__main__":
    main()