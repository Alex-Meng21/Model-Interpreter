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
            #error_msg = e.__str__()
            raise GrinParseError

        except GrinLexError as f: #come back to catching the exceptions
            #error_msg = f.__str__()
            raise GrinLexError

    return grin_statements

def read_input_for_testing(statement:str):

    token_list = []
    lines = statement.strip().split('\n')
    parsed_objs = parse(lines)
    for i in parsed_objs:
        token_list.append(list(i))

    return token_list






