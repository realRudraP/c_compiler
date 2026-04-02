from src.lexer.lexer import Lexer
from src.lexer.token import Token
from src.error.syntactical import SyntacticalError

class SyntaxAnalyzer:
    def __init__(self, source_code: str):
        self.lexer = Lexer(source_code)
        self.current_token = None
        self.peek_token = None
        self.errors = []
        self.advance()

    def advance(self):
        self.current_token = self.peek_token or self.lexer.get_next_token()
        self.peek_token = self.lexer.get_next_token()

    