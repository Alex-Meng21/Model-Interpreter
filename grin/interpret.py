from grin import *


def interpret_grin_identifiers(token_list):
    variable_dict = {}
    for token in token_list:

        if token[0].text() == 'LET':
            var = token[1].text()
            if token[2].value() is None:
                variable_dict[var] = 0
            else:
                variable_dict[var] = token[2].value()
        elif token[0].text() == 'PRINT' and (token[1].text() in variable_dict):
            print(variable_dict[token[1].text()])

    return variable_dict


def interpret_arithmetic(token_list):

    for token in token_list:

        pass