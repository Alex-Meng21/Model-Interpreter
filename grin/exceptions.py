from grin import parsing, location

class GrinRuntimeError(Exception):

    def __init__(self, message):
        super.__init__(message)
        self.message = message

class ParseError(Exception):

    def __init__(self, message):
        super.__init__(message)
        self.message = message