from utils import parse_program,evaluate_program

def top_level_parser():
    lines = []
    while True:
        try:
            user_input = input()
            if(user_input):
                lines.append(user_input)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    return lines
    

def main():
    statements = top_level_parser()
    parsed_statements = parse_program(statements)
    evaluate_program(parsed_statements)
    
    return

if __name__=="__main__":
    main()