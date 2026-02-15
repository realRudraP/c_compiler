from enum import Enum, auto


class TokenType(Enum):
    # Keywords

    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()

    # Identifier and literals

    IDENTIFIER = auto()
    INTEGER_LITERAL = auto()
    FLOAT_LITERAL = auto()
    CHAR_LITERAL = auto()
    STRING_LITERAL = auto()

    # Operators

    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_NOT = auto()

    # Symbols and delimiters
    SEMICOLON = auto()
    COMMA = auto()
    LEFT_PARAN = auto()  # (
    RIGHT_PARAN = auto()  # )
    LEFT_BRACE = auto()  # {
    RIGHT_BRACE = auto()  # }
    LEFT_BRACKET = auto()  # [
    RIGHT_BRACKET = auto()  # ]

    # Specials
    EOF = auto()
    NEWLINE = auto()
