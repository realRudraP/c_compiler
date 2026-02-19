class BaseError:
    def __init__(self, message, column, line):
        self.message = message
        self.column = column
        self.line = line

    def __str__(self):
        return f"Error at line {self.line}, column {self.column}: {self.message}"
