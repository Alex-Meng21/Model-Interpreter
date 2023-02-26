from grin import *

def read_input():

    grin_statement = input()

    lines = grin_statement.strip().split('\n')
    try:
        return list(parse(lines))
    except GrinParseError as e:
        print(f"Parse error on line {e.location.line_number}: {e.message}")
