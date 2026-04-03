from .token_types import TokenType

KEYWORDS = {
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'char': TokenType.CHAR,
    'void': TokenType.VOID,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'return': TokenType.RETURN,
    'do': TokenType.DO,
}

def is_keyword(word):
    return word in KEYWORDS

def get_keyword_token_type(word):
    return KEYWORDS.get(word)
