from grin.token import *
class GrinInterpreter:

    def __init__(self):
        self.var_dictionary = {}
        self.label_dictionary = {}
        self.counter = 0

    def obtain_value_from_dict(self, key):

        value = self.var_dictionary[key]
        return value

    def assign_labels(self, token_list):
        i = 1
        for token in token_list:
            if token[0].kind() == GrinTokenKind.IDENTIFIER:
                if token[1].kind() == GrinTokenKind.COLON:
                    var = token[0].text()
                    self.label_dictionary[var] = i
            i += 1



    def jump_without_conditionals(self, label, token_list):

        if label.kind() == GrinTokenKind.LITERAL_STRING:
            if label.value() not in self.label_dictionary.keys():
                raise RuntimeError("Cannot got to label that doesn't exist")

            self.counter = self.label_dictionary.get(label.value(), 0)

        elif label.kind() == GrinTokenKind.IDENTIFIER:
            if label.text() not in self.var_dictionary:
                raise RuntimeError("variable does not exist")
            value = self.var_dictionary.get(label.text(), 0)

            if isinstance(value, str):
                if value in self.label_dictionary:
                    self.counter = self.label_dictionary[value]
            elif isinstance(value, int):
                if value == 0:
                    raise RuntimeError(" Infinite loop")

                elif (value + self.counter > len(token_list)) or value + self.counter <= 0:
                    raise RuntimeError(f'Jumping out of range')

                self.counter += value

            else:
                raise RuntimeError("GOTO must be followed by an integer or string")

        else:

            if label.value() == 0:
                raise RuntimeError("infinite loop")
            elif (label.value() + self.counter) > len(token_list) or (
                    self.counter + label.value()) <= 0:
                raise RuntimeError("out of range")  # custom exception

            self.counter += label.value()



    def process_grin(self, token_list):
        j = 0
        while self.counter < len(token_list):
            token = token_list[self.counter]
            operation = token[j].text()
            if token[0].text() == 'END':
                self.counter = len(token_list)

            elif token[1].text() not in self.var_dictionary and token[1].kind() == GrinTokenKind.IDENTIFIER:
                self.var_dictionary[token[1].text()] = 0

    #interpreting identifier statements
            if operation == 'LET':
                var = token[1].text()
                if token[2].value() is None:
                    self.var_dictionary[var] = 0
                else:
                    self.var_dictionary[var] = token[2].value()
                self.counter +=1

            elif token[0].kind() == GrinTokenKind.IDENTIFIER: #handling labels
                self.counter += 1

        #interpreting prints

            elif operation == 'PRINT':
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

            try:
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
                    thing = token[1]
                    self.jump_without_conditionals(thing, token_list)


                elif operation == "GOTO" and len(token) > 2:
                    pass



            except TypeError:
                raise TypeError('Tried arithmetic options that did not work')

            except ZeroDivisionError:
                raise ZeroDivisionError("Cannot divide by zero")

            except ValueError:
                raise ValueError("value error occured")

            except IndexError:
                raise RuntimeError














