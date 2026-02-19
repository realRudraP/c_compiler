from src.error.base import BaseError


class SyntacticalError(BaseError):
    def __init__(self, message, line, coulmn):
        super().__init__(message, coulmn, line)
