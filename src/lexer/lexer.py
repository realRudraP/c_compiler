from .token import Token
from .token_types import TokenType
from .keywords import KEYWORDS
from ..error.lexical import LexicalError


class Lexer:
    def __init__(self, source_code) -> None:
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = source_code[0] if source_code else None
        self.errors = []

    """Move to the next character"""

    def advance(self):

        if self.current_char is None:
            return

        if self.current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1

        if self.pos < len(self.source):
            self.current_char = self.source[self.pos]
        else:
            self.current_char = None


    """Look at the next character without advancing the lexer status"""

    def peek(self, offset=1):
        peek_pos = self.pos + offset
        return self.source[peek_pos] if peek_pos < len(self.source) else None

    """Skip single-line and multi-line comments"""

    def skip_comment(self):
        if self.current_char == "/" and self.peek() == "/":
            while self.current_char is not None and self.current_char != "\n":
                self.advance()
        elif self.current_char == "/" and self.peek() == "*":
            self.advance()  # Skip '/'
            self.advance()  # Skip '*'
            while True:
                if self.current_char is None:
                    self.errors.append(
                        LexicalError(
                            "Unterminated multi-line comment", self.line, self.column
                        )
                    )
                if self.current_char == "*" and self.peek() == "/":
                    self.advance()  # Skip '*'
                    self.advance()  # Skip '/'
                    break
                else:
                    self.advance()
