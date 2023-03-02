import unittest
from grin import *
from grin import GrinInterpreter

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

        token_list = read_input_for_testing("X: PRINT A")
        self.interpret.process_grin(token_list)
        a = self.interpret.label_dictionary[token_list[0][0].text()]
        self.assertEqual(a, 1)

if __name__ == '__main__':
    unittest.main()
