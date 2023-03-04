from grin.token import *
class GrinInterpreter:

    def __init__(self):
        self.var_dictionary = {}
        self.label_dictionary = {}
        self.gosub_indexes = []
        self.counter = 0


    def obtain_value_from_dict(self, token):

        if token.kind() == GrinTokenKind.IDENTIFIER:
            value = self.var_dictionary.get(token.value(), 0)
        else:
            value = token.value() #or value()
        return value

    def assign_labels(self, token_list):
        i = 1
        for token in token_list:
            if token[0].kind() == GrinTokenKind.IDENTIFIER:
                if token[1].kind() == GrinTokenKind.COLON:
                    var = token[0].text()
                    self.label_dictionary[var] = i-1
            i += 1



    def jump_lines(self, label, token_list):

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
        i = 0
        while self.counter < len(token_list):
            #print('line:', self.counter, self.gosub_indexes)

            token = token_list[self.counter]

            if token[i].kind() == GrinTokenKind.END:
                break

            elif token[i].kind() == GrinTokenKind.RETURN:
                if len(self.gosub_indexes) == 0:
                    raise RuntimeError("Return statements must have previous GOSUB")
                else:
                    self.counter = self.gosub_indexes[-1]
                    del self.gosub_indexes[-1]
                    i = 0

            elif token[i].kind() == GrinTokenKind.IDENTIFIER:
                # handling labels
                i += 2

    #interpreting identifier statements
            elif token[i].kind() == GrinTokenKind.LET:

                var = token[i+1].text()
                if token[i+2].value() is None:
                    self.var_dictionary[var] = 0
                else:
                    self.var_dictionary[var] = token[i+2].value()
                self.counter += 1
                i = 0

#assigning identifiers to 0 if undefined
            elif len(token) > i+1 and token[i + 1].text() not in self.var_dictionary and token[i + 1].kind() == GrinTokenKind.IDENTIFIER:
                self.var_dictionary[token[i + 1].text()] = 0
                i = 0

        #interpreting prints

            elif token[i].kind() == GrinTokenKind.PRINT:
                if token[i+1].text() in self.var_dictionary:
                    print(self.var_dictionary[token[i+1].text()])
                elif token[i+1].kind() == GrinTokenKind.LITERAL_STRING or \
                        token[i+1].kind() == GrinTokenKind.LITERAL_INTEGER or \
                        token[i+1].kind() == GrinTokenKind.LITERAL_FLOAT:
                    print(token[i+1].text())
                else:
                    self.var_dictionary[token[i+1].text()] = 0
                    print('0')

                self.counter += 1
                i = 0

        #interpreting arithmetic

            try:
                if token[i].kind() == GrinTokenKind.ADD :
                    if isinstance(token[i+2].value(),(int,float)):
                        self.var_dictionary[token[i+1].text()] = self.var_dictionary.get(token[i+1].text(),0) + token[i+2].value()

                    elif isinstance(token[i+2].value(), str) and token[i+2].kind() != GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[i+1].text()] = self.var_dictionary.get(token[i+1].text(),0) + token[i+2].value()

                    elif token[i+2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[i+1].text()] = (self.var_dictionary.get(token[i+1].text(),0) +
                                                        self.var_dictionary.get(token[i+2].value(),0))

                    self.counter +=1
                    i = 0
                elif token[i].kind() == GrinTokenKind.SUB :
                    if isinstance(token[i+2].value(), (int, float)):
                        self.var_dictionary[token[i+1].text()] = self.var_dictionary.get(token[i+1].text(), 0) - token[i+2].value()

                    elif token[i+2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[i+1].text()] = (self.var_dictionary.get(token[i+1].text(), 0) -
                                                                self.var_dictionary.get(token[i+2].value(), 0))
                    self.counter +=1
                    i = 0
                elif token[i].kind() == GrinTokenKind.MULT :
                    if isinstance(token[i+2].value(), (int,float)):
                        self.var_dictionary[token[i+1].text()] = self.var_dictionary.get(token[i+1].text(), 0) * token[i+2].value()

                    elif isinstance(token[i+2].value(), str) and token[i+2].kind() != GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[i+1].text()] = self.var_dictionary.get(token[i+1].text(), 0) * token[i+2].value()

                    elif token[i+2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[i+1].text()] = (self.var_dictionary.get(token[i+1].text(), 0) *
                                                                self.var_dictionary.get(token[i+2].text(), 0))
                    self.counter +=1
                    i = 0

                elif token[i].kind() == GrinTokenKind.DIV:
                    if isinstance(token[i+2].value(), int) and isinstance(self.var_dictionary[token[i+1].text()], int):
                        self.var_dictionary[token[i+1].text()] = self.var_dictionary.get(token[i+1].text(), 0) // token[i+2].value()

                    elif isinstance(token[i+2].value(), (float, int)):
                        self.var_dictionary[token[i+1].text()] = self.var_dictionary.get(token[i+1].text(), 0) / token[i+2].value()

                    elif token[i+2].kind() == GrinTokenKind.IDENTIFIER:
                        self.var_dictionary[token[i+1].text()] = (self.var_dictionary.get(token[i+1].text(), 0) /
                                                                self.var_dictionary.get(token[i+2].value(), 0))
                    self.counter +=1
                    i = 0

                #reading input

                elif token[i].kind() == GrinTokenKind.INNUM:
                    num_input = float(input())
                    if num_input.is_integer():
                        self.var_dictionary[token[i+1].text()] = int(num_input)
                    else:
                        self.var_dictionary[token[i+1].text()] = num_input
                    self.counter += 1
                    i = 0

                elif token[i].kind() == GrinTokenKind.INSTR:
                    str_input = input()
                    self.var_dictionary[token[i+1].text()] = str_input
                    self.counter += 1
                    i = 0

                #Altering Control Flow without conditional statements

                elif token[i].kind() == GrinTokenKind.GOTO and len(token) == 2:
                    thing = token[i+1]
                    self.jump_lines(thing, token_list)
                    i = 0

                #Altering control flow with conditional statements

                elif token[i].kind() == GrinTokenKind.GOTO and len(token) > 2:
                    comparison = token[i+4].kind()
                    right_side = token[i+5]
                    left_side = token[i+3]
                    left_val = self.obtain_value_from_dict(left_side)
                    right_val = self.obtain_value_from_dict(right_side)
                    if comparison == GrinTokenKind.EQUAL:
                        if left_val == right_val:
                            self.jump_lines(token[i+1], token_list)
                        else:
                            self.counter +=1

                    elif comparison == GrinTokenKind.LESS_THAN_OR_EQUAL:
                        if left_val <= right_val:
                            self.jump_lines(token[i+1], token_list)
                        else:
                            self.counter +=1

                    elif comparison == GrinTokenKind.GREATER_THAN:
                        if left_val > right_val:
                            self.jump_lines(token[i+1], token_list)
                        else:
                            self.counter += 1

                    elif comparison == GrinTokenKind.LESS_THAN:
                        if left_val < right_val:
                            self.jump_lines(token[i+1], token_list)
                        else:
                            self.counter +=1

                    elif comparison == GrinTokenKind.GREATER_THAN_OR_EQUAL:
                        if left_val >= right_val:
                            self.jump_lines(token[i+1], token_list)
                        else:
                            self.counter += 1

                    elif comparison == GrinTokenKind.NOT_EQUAL:
                        if left_val != right_val:
                            self.jump_lines(token[i+1], token_list)
                        else:
                            self.counter += 1
                    i = 0

                #subroutines without conditions
                elif token[i].kind() == GrinTokenKind.GOSUB and len(token) == 2:
                    index = self.counter + 1
                    self.gosub_indexes.append(index)
                    thing = token[i+1]
                    self.jump_lines(thing, token_list)
                    i = 0

                #subroutines with conditions
                elif token[i].kind() == GrinTokenKind.GOSUB and len(token) > 2:
                    comparison = token[i + 4].kind()
                    right_side = token[i + 5]
                    left_side = token[i + 3]
                    left_val = self.obtain_value_from_dict(left_side)
                    right_val = self.obtain_value_from_dict(right_side)
                    if comparison == GrinTokenKind.EQUAL:
                        if left_val == right_val:
                            index = self.counter + 1
                            self.gosub_indexes.append(index)
                            self.jump_lines(token[i + 1], token_list)
                        else:
                            self.counter += 1

                    elif comparison == GrinTokenKind.LESS_THAN_OR_EQUAL:
                        if left_val <= right_val:
                            index = self.counter + 1
                            self.gosub_indexes.append(index)
                            self.jump_lines(token[i + 1], token_list)
                        else:
                            self.counter += 1

                    elif comparison == GrinTokenKind.GREATER_THAN:
                        if left_val > right_val:
                            index = self.counter + 1
                            self.gosub_indexes.append(index)
                            self.jump_lines(token[i + 1], token_list)
                        else:
                            self.counter += 1

                    elif comparison == GrinTokenKind.LESS_THAN:
                        if left_val < right_val:
                            index = self.counter + 1
                            self.gosub_indexes.append(index)
                            self.jump_lines(token[i + 1], token_list)
                        else:
                            self.counter += 1

                    elif comparison == GrinTokenKind.GREATER_THAN_OR_EQUAL:
                        if left_val >= right_val:
                            index = self.counter + 1
                            self.gosub_indexes.append(index)
                            self.jump_lines(token[i + 1], token_list)
                        else:
                            self.counter += 1

                    elif comparison == GrinTokenKind.NOT_EQUAL:
                        if left_val != right_val:
                            index = self.counter + 1
                            self.gosub_indexes.append(index)
                            self.jump_lines(token[i + 1], token_list)
                        else:
                            self.counter += 1
                    i = 0

            except TypeError:
                raise TypeError('Tried commands on invalid types: int to string or float to string')

            except ZeroDivisionError:
                raise ZeroDivisionError("Cannot divide by zero")

            except ValueError:
                raise ValueError("value error occured")

            except IndexError as e:
                print(e)














