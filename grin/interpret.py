from grin.token import *
class GrinInterpreter:

    def __init__(self):
        self.var_dictionary = {}
        self.label_dictionary = {}

    def obtain_value_from_dict(self, key):

        value = self.var_dictionary[key]
        return value
    def interpret_grin_identifiers(self, token_list):

        for token in token_list:
            if token[1].text() not in self.var_dictionary and token[1].kind() == GrinTokenKind.IDENTIFIER:
                self.var_dictionary[token[1].text()] = 0

            if token[0].text() == 'LET':
                var = token[1].text()
                if token[2].value() is None:
                    self.var_dictionary[var] = 0
                else:
                    self.var_dictionary[var] = token[2].value()

        return self.var_dictionary

    def interpret_arithmetic(self, token_list):

        for token in token_list:
            operation = token[0].text()

            try:
                if operation == 'ADD' :
                    if isinstance(token[2].value(),(int,float)):
                        self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(),0) + token[2].value()

                    elif isinstance(token[2].value(), str) and token[2].kind() != GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(),0) + token[2].value()

                    elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(),0) +
                                                                self.var_dictionary.get(token[2].value(),0))
                elif operation == 'SUB' :
                    if isinstance(token[2].value(), (int, float)):
                        self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) - token[2].value()

                    elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(), 0) -
                                                                self.var_dictionary.get(token[2].value(), 0))
                elif operation == 'MULT' :
                    if isinstance(token[2].value(), (int,float)):
                        self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) * token[2].value()

                    elif isinstance(token[2].value(), str) and token[2].kind() != GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) * token[2].value()

                    elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(), 0) *
                                                                self.var_dictionary.get(token[2].text(), 0))
                elif operation == 'DIV':
                    if isinstance(token[2].value(), int) and isinstance(self.var_dictionary[token[1].text()], int):
                        self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) // token[2].value()

                    elif isinstance(token[2].value(), (float, int)):
                        self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) / token[2].value()

                    elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(), 0) /
                                                                self.var_dictionary.get(token[2].value(), 0))


            except TypeError:
                raise TypeError

            except ZeroDivisionError as z:
                print(z)

        return self.var_dictionary
    def interpret_input(self, token_list):

        for token in token_list:
            command = token[0].text()
            if command == "INNUM":
                try:
                    num_input = float(input())
                    if num_input.is_integer():
                        self.var_dictionary[token[1].text()] = int(num_input)
                    else:
                        self.var_dictionary[token[1].text()] = num_input
                except ValueError:
                    raise ValueError

            elif command == "INSTR":
                str_input = input()
                self.var_dictionary[token[1].text()] = str_input

        return self.var_dictionary


    def print_grin(self, token_list):
        for token in token_list:

            if token[0].text() == 'PRINT':
                if token[1].text() in self.var_dictionary:
                    print(self.var_dictionary[token[1].text()])
                elif token[1].kind() == GrinTokenKind.LITERAL_STRING or \
                        token[1].kind() == GrinTokenKind.LITERAL_INTEGER or \
                        token[1].kind() == GrinTokenKind.LITERAL_FLOAT:
                    print(token[1].text())
                else:
                    print('0')


