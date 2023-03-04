# project3.py
#
# ICS 33 Winter 2023
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

from grin import *


def main() -> None:
    try:
        myGrin = GrinInterpreter()
        token_list = read_input()
        myGrin.assign_labels(token_list)
        myGrin.process_grin(token_list)

    except ParseError as e:
        print(e)
    except GrinLexError as f:
        print(f)


    except ZeroDivisionError:
        pass



if __name__ == '__main__':
    main()
