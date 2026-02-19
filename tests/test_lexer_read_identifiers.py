import unittest
from src.lexer.lexer import Lexer
from src.lexer.token import Token
from src.lexer.token_types import TokenType


class TestLexerReadIdentifiers(unittest.TestCase):
    def test_read_keywords(self):
        source_code = """
            int float char void if else while for return
        """
        lexer = Lexer(source_code)
        expected_tokens = [
            Token(TokenType.INT, "int", 2, 13),
            Token(TokenType.FLOAT, "float", 2, 17),
            Token(TokenType.CHAR, "char", 2, 23),
            Token(TokenType.VOID, "void", 2, 28),
            Token(TokenType.IF, "if", 2, 33),
            Token(TokenType.ELSE, "else", 2, 36),
            Token(TokenType.WHILE, "while", 2, 41),
            Token(TokenType.FOR, "for", 2, 47),
            Token(TokenType.RETURN, "return", 2, 51),
        ]
        lexer.skip_whitespace()
        for expected_token in expected_tokens:
            token = lexer.read_identifier()
            self.assertEqual(token, expected_token)
            lexer.skip_whitespace()

    def test_read_identifiers(self):
        source_code = """
            myVar _temp var123
        """
        lexer = Lexer(source_code)
        expected_tokens = [
            Token(TokenType.IDENTIFIER, "myVar", 2, 13),
            Token(TokenType.IDENTIFIER, "_temp", 2, 19),
            Token(TokenType.IDENTIFIER, "var123", 2, 25),
        ]
        lexer.skip_whitespace()
        for expected_token in expected_tokens:
            token = lexer.read_identifier()
            self.assertEqual(token, expected_token)
            lexer.skip_whitespace()

    def test_invalid_identifier_starting_with_digit(self):
        source_code = """
            123abc
        """
        lexer = Lexer(source_code)
        expected_error_message = "Identifiers cannot start with a digit"
        lexer.skip_whitespace()
        token = lexer.read_identifier()
        self.assertEqual(len(lexer.collected_errors), 1)
        self.assertEqual(token.type, TokenType.IDENTIFIER)
        self.assertEqual(token.value, "123abc")
        self.assertEqual(lexer.collected_errors[0].message, expected_error_message)

    def test_identifiers_with_only_underscores(self):
        source_code = """
            ___
        """
        lexer = Lexer(source_code)
        expected_token = Token(TokenType.IDENTIFIER, "___", 2, 13)
        lexer.skip_whitespace()
        token = lexer.read_identifier()
        self.assertEqual(token, expected_token)

    def test_single_underscore_identifier(self):
        source_code = """
            _
        """
        lexer = Lexer(source_code)
        expected_token = Token(TokenType.IDENTIFIER, "_", 2, 13)
        lexer.skip_whitespace()
        token = lexer.read_identifier()
        self.assertEqual(token, expected_token)

    def test_identifier_at_eof(self):
        source_code = "myVar"
        lexer = Lexer(source_code)
        expected_token = Token(TokenType.IDENTIFIER, "myVar", 1, 1)
        token = lexer.read_identifier()
        self.assertEqual(token, expected_token)
        self.assertIsNone(lexer.current_char)

    def test_identifier_followed_by_operator(self):
        lexer = Lexer("myVar+")
        token = lexer.read_identifier()
        self.assertEqual(token.value, "myVar")
        self.assertEqual(lexer.current_char, "+")  # Should stop at operator

    def test_keywords_case_sensitive(self):
        lexer = Lexer("Int FLOAT Char")
        token1 = lexer.read_identifier()
        lexer.skip_whitespace()
        token2 = lexer.read_identifier()
        lexer.skip_whitespace()
        token3 = lexer.read_identifier()
        self.assertEqual(token1.type, TokenType.IDENTIFIER)
        self.assertEqual(token1.value, "Int")
        self.assertEqual(token2.type, TokenType.IDENTIFIER)
        self.assertEqual(token2.value, "FLOAT")
        self.assertEqual(token3.type, TokenType.IDENTIFIER)
        self.assertEqual(token3.value, "Char")

    def test_very_long_identifier(self):
        long_identifier = "a" * 1000
        lexer = Lexer(long_identifier)
        expected_token = Token(TokenType.IDENTIFIER, long_identifier, 1, 1)
        token = lexer.read_identifier()
        self.assertEqual(token, expected_token)

    def test_identifier_with_mixed_underscores_and_numeric(self):
        source_code = "_my_Var_123_"
        lexer = Lexer(source_code)
        expected_token = Token(TokenType.IDENTIFIER, "_my_Var_123_", 1, 1)
        token = lexer.read_identifier()
        self.assertEqual(token, expected_token)

    def test_multiple_identifiers_in_a_row(self):
        source_code = "var1 var2 var3"
        lexer = Lexer(source_code)
        expected_tokens = [
            Token(TokenType.IDENTIFIER, "var1", 1, 1),
            Token(TokenType.IDENTIFIER, "var2", 1, 6),
            Token(TokenType.IDENTIFIER, "var3", 1, 11),
        ]
        for expected_token in expected_tokens:
            token = lexer.read_identifier()
            self.assertEqual(token, expected_token)
            lexer.skip_whitespace()
