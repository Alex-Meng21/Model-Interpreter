

class GrinRuntimeError(Exception):
    """A custom exception raised on all runtime errors in Grin"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

