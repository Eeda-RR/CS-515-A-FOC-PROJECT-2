from utils import parse_program,evaluate_program

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
    parsed_statements = parse_program(statements)
    evaluate_program(parsed_statements)
    return

if __name__=="__main__":
    main()