from utils import get_parsed_statements

def top_level_parser():
    lines = []
    while True:
        user_input = input()
        # if user pressed Enter without a value, break out of loop
        if user_input == '':
            break
        else:
            lines.append(user_input)
    return lines
    

def main():
    statements = top_level_parser()
    parsed_statements = get_parsed_statements(statements)     
    for parsed_statement in parsed_statements:
        print(parsed_statement)

if __name__=="__main__":
    main()