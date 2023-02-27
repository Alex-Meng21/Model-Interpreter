from grin import *

def read_input():
    grin_statements = []

    while True:
        grin_statement = input()
        lines = grin_statement.strip().split('\n')

        if '.' in lines:
            break
        try:
            parsed_objs = parse(lines)
            for i in parsed_objs:
                grin_statements.append(list(i))

        except GrinParseError as e:
            print(e)

        except GrinLexError as f: #come back to catching the exceptions
            print(f)

    return grin_statements





