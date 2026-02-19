from src.error.base import BaseError


class LexicalError(BaseError):
    def __init__(self, message, line, column):
        super().__init__(message, column, line)
