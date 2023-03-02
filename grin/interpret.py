from grin.token import *
class GrinInterpreter:

    def __init__(self):
        self.var_dictionary = {}
        self.label_dictionary = {}
        self.counter = 0

    def obtain_value_from_dict(self, key):

        value = self.var_dictionary[key]
        return value

    def process_grin(self, token_list):

        while self.counter < len(token_list):
            token = token_list[self.counter]
            operation = token[0].text()

            if token[1].text() not in self.var_dictionary and token[1].kind() == GrinTokenKind.IDENTIFIER:
                self.var_dictionary[token[1].text()] = 0
        #interpreting identifier statements
            if operation == 'LET':
                var = token[1].text()
                if token[2].value() is None:
                    self.var_dictionary[var] = 0

                else:
                    self.var_dictionary[var] = token[2].value()
                self.counter += 1

        #interpreting labels
            elif token[1].kind() == GrinTokenKind.COLON:
                var = token[0].text()
                self.label_dictionary[var] = token[1].location().line()
                self.counter += 1

        #interpreting prints

            elif token[0].text() == 'PRINT':
                if token[1].text() in self.var_dictionary:
                    print(self.var_dictionary[token[1].text()])
                elif token[1].kind() == GrinTokenKind.LITERAL_STRING or \
                        token[1].kind() == GrinTokenKind.LITERAL_INTEGER or \
                        token[1].kind() == GrinTokenKind.LITERAL_FLOAT:
                    print(token[1].text())
                else:
                    print('0')

                self.counter += 1

        #interpreting arithmetic


            if operation == 'ADD' :
                if isinstance(token[2].value(),(int,float)):
                    self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(),0) + token[2].value()

                elif isinstance(token[2].value(), str) and token[2].kind() != GrinTokenKind.IDENTIFIER:
                    self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(),0) + token[2].value()

                elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                    self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(),0) +
                                                    self.var_dictionary.get(token[2].value(),0))
                self.counter +=1
            elif operation == 'SUB' :
                if isinstance(token[2].value(), (int, float)):
                    self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) - token[2].value()

                elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                    self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(), 0) -
                                                            self.var_dictionary.get(token[2].value(), 0))
                self.counter +=1
            elif operation == 'MULT' :
                if isinstance(token[2].value(), (int,float)):
                    self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) * token[2].value()

                elif isinstance(token[2].value(), str) and token[2].kind() != GrinTokenKind.IDENTIFIER:
                    self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) * token[2].value()

                elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                    self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(), 0) *
                                                            self.var_dictionary.get(token[2].text(), 0))
                self.counter +=1
            elif operation == 'DIV':
                if isinstance(token[2].value(), int) and isinstance(self.var_dictionary[token[1].text()], int):
                    self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) // token[2].value()

                elif isinstance(token[2].value(), (float, int)):
                    self.var_dictionary[token[1].text()] = self.var_dictionary.get(token[1].text(), 0) / token[2].value()

                elif token[2].kind() == GrinTokenKind.IDENTIFIER:
                    self.var_dictionary[token[1].text()] = (self.var_dictionary.get(token[1].text(), 0) /
                                                            self.var_dictionary.get(token[2].value(), 0))
                self.counter +=1

            #reading input

            elif operation == "INNUM":
                num_input = float(input())
                if num_input.is_integer():
                    self.var_dictionary[token[1].text()] = int(num_input)
                else:
                    self.var_dictionary[token[1].text()] = num_input
                self.counter += 1

            elif operation == "INSTR":
                str_input = input()
                self.var_dictionary[token[1].text()] = str_input
                self.counter += 1

            #Altering Control Flow without conditional statements

            elif operation == "GOTO" and len(token) == 2:

                if token[1].kind() == GrinTokenKind.LITERAL_INTEGER:
                    if token[1].value() == 0:
                        raise RuntimeError("infinite loop")
                    elif (token[1].value() + self.counter) > len(token_list) or (self.counter + token[1].value()) <= 0:
                        raise RuntimeError("out of range") #custom exception
                    else:
                        self.counter += token[1].value()

                elif token[1].kind() == GrinTokenKind.LITERAL_STRING:
                    if token[1].text() not in self.label_dictionary:
                        raise RuntimeError("Cannot got to label that doesn't exist")
                    else:
                        self.counter = self.label_dictionary[token[1].text()]

                elif token[1].kind() == GrinTokenKind.IDENTIFIER:
                    dict_key = token[1].text()
                    value_from_dict = self.var_dictionary[dict_key]
                    if isinstance(value_from_dict, int) and (value_from_dict + self.counter < len(token_list)) and (
                            value_from_dict + self.counter > 0):
                        self.counter += value_from_dict
                    elif value_from_dict in self.label_dictionary:
                        self.counter = self.label_dictionary[value_from_dict]
                    else:
                        raise RuntimeError("OUT of range")

            elif operation == "GOTO" and len(token) > 2:
                pass




            """except TypeError:
                raise TypeError

            except ZeroDivisionError:
                raise ZeroDivisionError

            except ValueError:
                raise ValueError

            else:
                if operation == 'END':
                    pass"""










