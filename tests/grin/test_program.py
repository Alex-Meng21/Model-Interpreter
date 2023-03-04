import unittest
from grin import *
from grin import GrinInterpreter
from project3 import main

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.interpret = GrinInterpreter()

    def test_0_for_unassigned(self):
        token_list = list(parse(["PRINT A"]))
        self.interpret.process_grin(token_list)
        self.assertEqual(self.interpret.var_dictionary[token_list[0][1].text()], 0)
        self.assertEqual(token_list[0][1].text(), 'A')

    def test_LET_statements(self):

        token_list = list(parse(["LET A 2"]))

        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 2)

    def test_add_integers(self):

        token_list = read_input_for_testing("LET A 2\nADD A 10")

        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 12)

    def test_add_strings(self):

        token_list = read_input_for_testing("LET A boo\nLET B lean\nADD A B")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 'boolean')

    def test_add_float_and_integer(self):

        token_list = read_input_for_testing("LET A 4.5\nADD A 2")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 6.5)

    def test_adding_floats(self):

        token_list = read_input_for_testing("LET A 4.5\nADD A 4.5")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 9.0)

    def test_adding_identifiers_with_value(self):

        token_list = read_input_for_testing("LET A 4.5\nLET B 4.5\nADD A B")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 9.0)

    def test_adding_identifiers_without_value(self):
        token_list = read_input_for_testing("LET A 4.5\nADD A B")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 4.5)

    def test_adding_identifiers_without_value_reversed(self):
        token_list = read_input_for_testing("LET A 4.5\nADD B A")
        self.interpret.process_grin(token_list)

        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual(b, 4.5)

    def test_subtracting_integers(self):
        token_list = read_input_for_testing("LET A 4\nSUB A 6")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, -2)

    def test_subtract_floats(self):
        token_list = read_input_for_testing("LET A 18.5\nSUB A 7.0")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 11.5)

    def test_subtract_int_and_float(self):
        token_list = read_input_for_testing("LET A 18\nSUB A 6.5")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 11.5)

    def test_multiply_integers(self):
        token_list = read_input_for_testing("LET A 10\nMULT A 2")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 20)

    def test_multiply_floats(self):
        token_list = read_input_for_testing("LET A 3.5\nMULT A 12.0")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 42.0)

    def test_multiply_float_and_integer(self):
        token_list = read_input_for_testing("LET A 3\nMULT A 12.5")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 37.5)

    def test_multiply_string_integer(self):
        token_list = read_input_for_testing("LET A Boo\nMULT A 3")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 'BooBooBoo')

    def test_multiply_integer_string(self):
        token_list = read_input_for_testing("LET A 3\nLET B hi\nMULT A B")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 'hihihi')

    def test_divide_integers(self):
        token_list = read_input_for_testing("LET A 7\nDIV A 2")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 3)

    def test_divide_floats(self):
        token_list = read_input_for_testing("LET A 7.5\nDIV A 3.0")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 2.5)

    def test_divide_float_and_int(self):
        token_list = read_input_for_testing("LET A 7.0\nLET B 2\nDIV A B")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 3.5)

    def test_combined_arithmetic(self):
        token_list = read_input_for_testing("LET A 4\nADD A 3\nLET B 5\nSUB B 3\nLET C 6\nMULT C B\nLET D 8\nDIV D 2")
        self.interpret.process_grin(token_list)

        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[2][1].text()]
        c = self.interpret.var_dictionary[token_list[4][1].text()]
        d = self.interpret.var_dictionary[token_list[6][1].text()]

        self.assertEqual((a,b,c,d), (7,2,12,4))
        self.assertEqual(self.interpret.counter, 8)

    def test_labels(self):

        token_list = read_input_for_testing("X:         PRINT A\n   CHUNK: ADD A 5")
        self.interpret.assign_labels(token_list)
        a = self.interpret.label_dictionary[token_list[0][0].text()]
        b = self.interpret.label_dictionary[token_list[1][0].text()]
        self.assertEqual((a,b), (0,1))

    def test_basic_goto(self):

        token_list = read_input_for_testing("LET A 1\nGOTO 2\nADD A 2\nADD A 4")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 5)

    def test_negative_goto(self):
        token_list = read_input_for_testing("LET Z 5\nGOTO 5\nLET C 4\nPRINT C\nPRINT Z\nEND\nPRINT C\nPRINT Z\nGOTO -6")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[2][1].text()]
        self.assertEqual((a,b), (5, 4))

    def test_goto_variable_int(self):
        token_list = read_input_for_testing("LET B 2\nGOTO B\nSUB B 2\nLET B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 5)

    def test_goto_if_equal_int(self):
        token_list = read_input_for_testing("LET B 2\nGOTO 2 IF B = 2\nSUB B 2\nLET B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 5)

    def test_goto_notequal_labels(self):
        token_list = read_input_for_testing("LET B 2\nLET A 1\nGOTO 2 IF B = A\nSUB B 2\nMULT B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 0)


    def test_less_than_equal_to_true(self):
        token_list = read_input_for_testing("LET B 2\nGOTO 3 IF B <= 3\nSUB B 2\nMULT B 5\nADD B 10")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 12)

    def test_less_than_equal_to_false(self):
        token_list = read_input_for_testing("LET B 3\nLET A 1\nGOTO 2 IF B <= A\nSUB B 2\nMULT B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 5)

    def test_greater_than_true(self):
        token_list = read_input_for_testing("LET B 2\nLET A 1.5\nGOTO 2 IF B > A\nSUB B 2\nMULT B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 10)

    def test_greater_than_false(self):
        token_list = read_input_for_testing("LET B 12\nGOTO 2 IF B > 3\nSUB B 2\nDIV B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 2)

    def test_less_than_true(self):
        token_list = read_input_for_testing("LET B adam\nLET A lex\nGOTO 2 IF B < A\nSUB B 2\nMULT B 3")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 'adamadamadam')

    def test_less_than_false(self):
        token_list = read_input_for_testing("LET B 12\nLET A 10\nGOTO 2 IF B < A\nADD B C\nMULT B 2")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 24)

    def test_greater_than_or_equal_to_true(self):
        token_list = read_input_for_testing("LET B 2\nLET A 1\nGOTO 2 IF B >= A\nSUB B 2\nMULT B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 10)

    def test_greater_than_or_equal_false(self):
        token_list = read_input_for_testing("LET B 2\nGOTO 2 IF B >= 3\nADD B 2\nMULT B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 20)

    def test_not_equal_true(self):
        token_list = read_input_for_testing("LET B Alex\nLET A yay\nGOTO 2 IF B <> A\nSUB B 2\nMULT B 3")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 'AlexAlexAlex')

    def test_not_equal_false(self):
        token_list = read_input_for_testing("LET B 2\nLET A 2\nGOTO 2 IF B <> A\nSUB B 2\nMULT B 5")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 0)

    def test_basic_gosub(self):
        token_list = read_input_for_testing("LET A 1\nGOSUB 3\nADD A 4\nEND\nLET A 6\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 10)


    def test_gosub_multiple_returns(self):
        token_list = read_input_for_testing("LET A 1\nGOSUB 5\nGOSUB 5\nPRINT A\nEND\nLET A 3\nRETURN\nPRINT A\nLET A 2\nGOSUB -4\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 3)

    def test_gosub_equal_true(self):
        token_list = read_input_for_testing("LET B 10\nGOSUB 3 IF B = 2\nSUB B 2\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 8)

    def test_gosub_equal_false(self):
        token_list = read_input_for_testing("LET B 4\nGOSUB 3 IF B = 2\nDIV B 2\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        self.assertEqual(a, 2)

    def test_gosub_not_equal_true(self):
        token_list = read_input_for_testing(
            "LET B 4\nLET A 10\nGOSUB 3 IF B <> A\nMULT A 2.5\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a,b),(5, 25))

    def test_gosub_less_than_true(self):
        token_list = read_input_for_testing(
            "LET A 4\nLET B 10\nGOSUB 3 IF A < B\nMULT A 2.5\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a, b), (10.0, 5))

    def test_gosub_less_than_false(self):
        token_list = read_input_for_testing(
            "LET A 4\nLET B 10\nGOSUB 3 IF B < A\nSUB A 2.5\nEND\nSUB B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual(a, 1.5)

    def test_gosub_less_than_eq_true(self):
        token_list = read_input_for_testing(
            "LET B 4\nLET A 10\nGOSUB 3 IF B <= A\nDIV A 2\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a, b), (5, 5))

    def test_gosub_less_eq_false(self):
        token_list = read_input_for_testing(
            "LET B 5\nLET A 2\nGOSUB 3 IF B <= A\nMULT A 2.5\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a, b), (5, 5))

    def test_gosub_greater_than_true(self):
        token_list = read_input_for_testing(
            "LET B alex\nLET A sauce\nGOSUB 3 IF B < A\nMULT A 2\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a, b), (5, 'saucesauce'))

    def test_gosub_greater_than_false(self):
        token_list = read_input_for_testing(
            "LET B 4\nLET A 10\nGOSUB 3 IF B > A\nSUB A 2.5\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a, b), (4, 7.5))

    def test_gosub_greater_than_eq_true(self):
        token_list = read_input_for_testing(
            "LET B 4\nLET A 4\nGOSUB 2 IF B >= A\nMULT A 2.5\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a, b), (4, 4))

    def test_gosub_greater_than_eq_false(self):
        token_list = read_input_for_testing(
            "LET B 4\nLET A 10\nGOSUB 3 IF B >= A\nMULT A 2.5\nEND\nLET B 5\nRETURN")
        self.interpret.process_grin(token_list)
        a = self.interpret.var_dictionary[token_list[0][1].text()]
        b = self.interpret.var_dictionary[token_list[1][1].text()]
        self.assertEqual((a, b), (4, 25))




if __name__ == '__main__':
    unittest.main()
