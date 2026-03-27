from .token import Token
from .token_types import TokenType
from .keywords import KEYWORDS, is_keyword
from src.error.syntactical import SyntacticalError
from src.error.lexical import LexicalError

from src.lexer import keywords


class Lexer:
    def __init__(self, source_code) -> None:
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = source_code[0] if source_code else None
        self.collected_errors = []

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

    # Number and text parsing methods

    def read_number(self):
        is_float = False
        number_str = ""
        number_column_position = self.column
        # This flag is decimal to ensure that a decimal point is not the first character in the number and that it is followed by digits
        leading_numbers_encountered = False
        # This flag is used to track if we have encountered a decimal point and are now expecting digits after it. If we encounter another decimal point or if we reach the end of the number without finding digits after the decimal point, we can raise an error.
        expecting_digit_after_decimal = False
        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char in "+-."
        ):
            if (
                not leading_numbers_encountered
                and self.current_char == "-"
                or self.current_char == "+"
            ):
                number_str += self.current_char
                self.advance()
                continue
            if self.current_char.isdigit():
                leading_numbers_encountered = True
            if self.current_char == ".":
                if not leading_numbers_encountered:
                    self.collected_errors.append(
                        LexicalError(
                            "Invalid number format: decimal point cannot be at the start",
                            self.line,
                            self.column,
                        )
                    )
                if is_float:
                    self.collected_errors.append(
                        LexicalError(
                            "Invalid number format: multiple decimal points",
                            self.line,
                            self.column,
                        )
                    )
                is_float = True
                expecting_digit_after_decimal = True
            if self.current_char.isdigit() and expecting_digit_after_decimal:
                expecting_digit_after_decimal = False
            number_str += self.current_char
            self.advance()
        if self.current_char is not None and self.current_char.isalpha():
            self.collected_errors.append(
                LexicalError(
                    "Invalid identifier: identifiers cannot start with a digit",
                    self.line,
                    self.column,
                )
            )
        if expecting_digit_after_decimal:
            self.collected_errors.append(
                LexicalError(
                    "Invalid number format: decimal point must be followed by digits",
                    self.line,
                    self.column,
                )
            )
        return Token(
            TokenType.FLOAT if is_float else TokenType.INT,
            number_str,
            self.line,
            number_column_position,
        )

    def read_identifier(self) -> Token:
        identifier_str = ""
        identifier_column_position = self.column
        if self.current_char is not None and self.current_char.isdigit():
            self.collected_errors.append(
                LexicalError(
                    "Identifiers cannot start with a digit",
                    self.line,
                    identifier_column_position,
                )
            )
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            identifier_str += self.current_char
            self.advance()

        if (token_type := keywords.get_keyword_token_type(identifier_str)) is not None:
            return Token(
                token_type, identifier_str, self.line, identifier_column_position
            )

        return Token(
            TokenType.IDENTIFIER, identifier_str, self.line, identifier_column_position
        )

    def read_string_literal(self) -> Token:
        string_literal = ""
        string_literal_column_position = self.column
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == "\n":
                self.collected_errors.append(
                    LexicalError(
                        "Unterminated string literal: newline encountered before closing '\"'",
                        self.line,
                        self.column,
                    )
                )
                break
            if (
                self.current_char == "\\"  # Used to handle escape sequences
            ):
                if self.peek() is None:
                    self.collected_errors.append(
                        LexicalError(
                            "Unterminated string literal: backslash at end of file",
                            self.line,
                            self.column,
                        )
                    )
                    break
                self.advance()
                if self.current_char in ['"', "\\", "n", "t", "r"]:
                    escape_sequences = {
                        '"': '"',
                        "\\": "\\",
                        "n": "\n",
                        "t": "\t",
                        "r": "\r",
                    }
                    string_literal += escape_sequences[self.current_char]
                else:
                    self.collected_errors.append(
                        LexicalError(
                            f"Invalid escape sequence: '\\{self.current_char}' is not a valid escape character",
                            self.line,
                            self.column,
                        )
                    )
                    string_literal += (
                        self.current_char
                    )  # add the operator so we can continue parsing the string
            else:
                string_literal += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()  # Skip the closing quote
        else:
            self.collected_errors.append(
                LexicalError(
                    "Unterminated string literal: reached end of source without closing '\"'",
                    self.line,
                    self.column,
                )
            )
        return Token(
            TokenType.STRING_LITERAL,
            string_literal,
            self.line,
            string_literal_column_position,
        )

    def read_special_symbol(self) -> Token:
        special_symbol_str = ""
        special_symbol_column_position = self.column
        SPECIAL_SYMBOLS = {'+':TokenType.PLUS, '-':TokenType.MINUS, '*':TokenType.MULTIPLY, '/':TokenType.DIVIDE,'(':TokenType.LEFT_PARAN,')':TokenType.RIGHT_PARAN,'{':TokenType.LEFT_BRACE,'}':TokenType.RIGHT_BRACE,'[':TokenType.LEFT_BRACKET,']':TokenType.RIGHT_BRACKET,';':TokenType.SEMICOLON,',':TokenType.COMMA, '=':TokenType.EQUAL, '!':TokenType.LOGICAL_NOT, '<':TokenType.LESS_THAN, '>':TokenType.GREATER_THAN, '&': TokenType.AMPERSAND, '|': TokenType.BITWISE_OR}
        MULTI_CHAR_SYMBOLS = {'==': TokenType.EQUAL_EQUAL, '!=': TokenType.NOT_EQUAL, '<=': TokenType.LESS_EQUAL, '>=': TokenType.GREATER_EQUAL, '&&': TokenType.LOGICAL_AND, '||': TokenType.LOGICAL_OR}
        while self.current_char is not None and self.current_char in SPECIAL_SYMBOLS.keys():
            special_symbol_str += self.current_char
            next_char = self.peek()
            if next_char in SPECIAL_SYMBOLS.keys():
                self.advance()
                special_symbol_str += self.current_char
            self.advance()
        if special_symbol_str in MULTI_CHAR_SYMBOLS:
            return Token(
                MULTI_CHAR_SYMBOLS[special_symbol_str],
                special_symbol_str,
                self.line,
                special_symbol_column_position,
            )
        elif special_symbol_str in SPECIAL_SYMBOLS:
            return Token(
                SPECIAL_SYMBOLS[special_symbol_str],
                special_symbol_str,
                self.line,
                special_symbol_column_position,
            )
        else:
            self.collected_errors.append(
                LexicalError(
                    f"Invalid special symbol: '{special_symbol_str}' is not a valid special symbol",
                    self.line,
                    special_symbol_column_position,
                )
            )
            return Token(
                TokenType.EOF, special_symbol_str, self.line, special_symbol_column_position
            )

    # Skip sections of source code

    """Skip both single-line and multi-line comments"""

    def skip_comment(self):
        if self.current_char == "/" and self.peek() == "/":
            while self.current_char is not None and self.current_char != "\n":
                self.advance()
            if self.current_char == "\n":
                self.advance()  # Skip the newline character after the comment
        elif self.current_char == "/" and self.peek() == "*":
            self.advance()  # Skip '/'
            self.advance()  # Skip '*'
            while True:
                if self.current_char is None:
                    self.collected_errors.append(
                        LexicalError(
                            "Unterminated comment: reached end of source without closing '*/'",
                            self.line,
                            self.column,
                        )
                    )
                    break
                if self.current_char == "*" and self.peek() == "/":
                    self.advance()  # Skip '*'
                    self.advance()  # Skip '/'
                    break
                self.advance()

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
