import unittest
from src.lexer.lexer import Lexer
from src.lexer.token import Token
from src.lexer.token_types import TokenType

class TestLexerReadFullCode(unittest.TestCase):
    def test_read_full_code(self):
        source_code = """
            int main() {
                int a = 5;
                float b = 3.14;
                if (a > b) {
                    return a;
                } else {
                    return b;
                }
            }
        """
        lexer = Lexer(source_code)
        expected_tokens = [
            Token(TokenType.INT, "int", 2, 13),
            Token(TokenType.IDENTIFIER, "main", 2, 17),
            Token(TokenType.LEFT_PARAN, "(", 2, 21),
            Token(TokenType.RIGHT_PARAN, ")", 2, 22),
            Token(TokenType.LEFT_BRACE, "{", 2, 24),
            Token(TokenType.INT, "int", 3, 17),
            Token(TokenType.IDENTIFIER, "a", 3, 21),
            Token(TokenType.EQUAL, "=", 3, 23),
            Token(TokenType.INTEGER_LITERAL, "5", 3, 25),
            Token(TokenType.SEMICOLON, ";", 3, 26),
            Token(TokenType.FLOAT, "float", 4, 17),
            Token(TokenType.IDENTIFIER, "b", 4, 23),
            Token(TokenType.EQUAL, "=", 4, 25),
            Token(TokenType.FLOAT_LITERAL, "3.14", 4, 27),
            Token(TokenType.SEMICOLON, ";", 4, 31),
            Token(TokenType.IF, "if", 5, 17),
            Token(TokenType.LEFT_PARAN, "(", 5, 20),
            Token(TokenType.IDENTIFIER, "a", 5, 21),
            Token(TokenType.GREATER_THAN, ">", 5, 23),
            Token(TokenType.IDENTIFIER, "b", 5, 25),
            Token(TokenType.RIGHT_PARAN, ")", 5, 26),
            Token(TokenType.LEFT_BRACE, "{", 5, 28),
            Token(TokenType.RETURN, "return", 6, 21),
            Token(TokenType.IDENTIFIER, "a", 6, 28),
            Token(TokenType.SEMICOLON, ";", 6, 29),
            Token(TokenType.RIGHT_BRACE, "}", 7, 17),
            Token(TokenType.ELSE, "else", 7, 19),
            Token(TokenType.LEFT_BRACE, "{", 7, 24),
            Token(TokenType.RETURN, "return", 8, 21),
            Token(TokenType.IDENTIFIER, "b", 8, 28),
            Token(TokenType.SEMICOLON, ";", 8, 29),
            Token(TokenType.RIGHT_BRACE, "}", 9, 17),
            Token(TokenType.RIGHT_BRACE, "}", 10, 13),
        ]
        lexer.skip_whitespace()
        for expected_token in expected_tokens:
            token = lexer.get_next_token()
            self.assertEqual(token, expected_token)
        self.assertEqual(lexer.collected_errors, [])