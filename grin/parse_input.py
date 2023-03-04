from grin import *



def read_input():
    """Reads the input from shell until . is entered and parses it before adding parsed tokens into
        a list

        Returns:
            grin_statements: a nested list containing all the tokens, with each statement in a sublist
    """
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

def read_input_for_testing(statement:str):

    """Same functionality as read_input() but for unit testing purposes

        Args:
            statement: a string of GRIN statements
        Returns:
            token_list: same as grin_statements from read_input()"""

    token_list = []
    lines = statement.strip().split('\n')
    parsed_objs = parse(lines)
    for i in parsed_objs:
        token_list.append(list(i))

    return token_list






