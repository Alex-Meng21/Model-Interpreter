from grin.token import *
from grin.errors import GrinRuntimeError
class GrinInterpreter:

    def __init__(self):
        """Initializes the interpreter to empty dictionaries and lists and the loop incrementer to 0"""
        self.var_dictionary = {}
        self.label_dictionary = {}
        self.gosub_indexes = []
        self.counter = 0


    def obtain_value_from_dict(self, token):
        """Gets the value from the arg: token, obtaining the value from the
        class attribute self.var_dictionary or the token's, value attribute

        Args:
            token: A single token object from the class GrinToken

        Returns:
            value: float, string, or integer value"""
        if token.kind() == GrinTokenKind.IDENTIFIER:
            value = self.var_dictionary.get(token.value(), 0)
        else:
            value = token.value()
        return value

    def assign_labels(self, token_list):
        """Loops through all the tokens from read_input() and assigns all the labels
        to their line numbers

        Args:
            token_list: a nested list containing list of token objects from the GrinToken class"""
        i = 1
        for token in token_list:
            if token[0].kind() == GrinTokenKind.IDENTIFIER:
                if token[1].kind() == GrinTokenKind.COLON:
                    var = token[0].text()
                    self.label_dictionary[var] = i-1
            i += 1



    def jump_lines(self, label, token_list):
        """Executes the GOTO and GOSUB commands. Raises GrinRunTimeError for invalid values
        following the keywords

        Args:
            label: the token object following the GOTO or GOSUB keyword
            token_list: a nested list containing list of token objects from the GrinToken class
        """

        if label.kind() == GrinTokenKind.LITERAL_STRING:
            if label.value() not in self.label_dictionary.keys():
                raise GrinRuntimeError(f"Error: Cannot got to label that doesn't exist: Line {self.counter+1}")

            self.counter = self.label_dictionary.get(label.value(), 0)
        elif label.kind() == GrinTokenKind.IDENTIFIER:
            if label.text() not in self.var_dictionary:
                raise GrinRuntimeError(f"Error: Variable does not exist so infinite loop would occur: Line {self.counter+1}")
            value = self.var_dictionary.get(label.text(), 0)

            if isinstance(value, str):
                if value in self.label_dictionary:
                    self.counter = self.label_dictionary[value]
            elif isinstance(value, int):
                if value == 0:
                    raise GrinRuntimeError(f"Error: Infinite loop -> Line: {self.counter+1}")

                elif (value + self.counter > len(token_list)) or value + self.counter <= 0:
                    raise GrinRuntimeError(f'Error: Jumping out of range of Grin statements Line: {self.counter+1}')

                self.counter += value

            else:
                raise GrinRuntimeError(f"Error: GOTO/GOSUB must be followed by an integer or string Line: {self.counter+1}")

        else:

            if label.value() == 0:
                raise GrinRuntimeError(f"Error: GOTO/GOSUB cannot be 0 -> infinite loop: Line{self.counter+1}")
            elif (label.value() + self.counter) > len(token_list) or (
                    self.counter + label.value()) <= 0:
                raise GrinRuntimeError(f'Error: Jumping out of range of Grin statements Line: {self.counter+1}')

            self.counter += label.value()



    def process_grin(self, token_list):
        """Loops through nested list of parsed token objects and executes all the
         Grin commands. Raises GrinRunTimeError for invalid arithmetic operations, inputs,
         or RETURN statements without GOSUB

         Args:
             token_list: a nested list containing lists of token objects from the GrinToken class
             returned by read_input()"""


        i = 0
        while self.counter < len(token_list):

            token = token_list[self.counter]

            if token[i].kind() == GrinTokenKind.END:
                break

            elif token[i].kind() == GrinTokenKind.RETURN:
                if len(self.gosub_indexes) == 0:
                    raise GrinRuntimeError(f"Error: Return statements must have previous GOSUB statement: error at Line {self.counter+1}")
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
                raise GrinRuntimeError(f'Error: Tried arithmetic commands on invalid types: Line {self.counter+1}')

            except ZeroDivisionError:
                raise GrinRuntimeError(f"Error: Cannot divide by zero: Line {self.counter+1}")

            except ValueError:
                raise GrinRuntimeError(f"Error: INNUM must be float or integers: Line {self.counter+1}")
















