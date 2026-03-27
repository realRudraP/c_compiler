import unittest
from src.lexer.lexer import Lexer
from src.lexer.token import TokenType
from src.lexer.token import Token


class TestLexerReadStringLiterals(unittest.TestCase):
    def test_read_string_literal(self):
        source = '"Hello, World!"'
        lexer = Lexer(source)
        expected_token = Token(TokenType.STRING_LITERAL, "Hello, World!", 1, 1)
        token = lexer.read_string_literal()
        self.assertEqual(token, expected_token)

    def test_unterminated_string_literal(self):
        source = '"Hello, World!'
        lexer = Lexer(source)
        expected_error_message = (
            "Unterminated string literal: reached end of source without closing '\"'"
        )
        token = lexer.read_string_literal()
        self.assertEqual(token.type, TokenType.STRING_LITERAL)
        self.assertEqual(token.value, "Hello, World!")
        self.assertEqual(len(lexer.collected_errors), 1)
        self.assertEqual(lexer.collected_errors[0].message, expected_error_message)

    def test_string_literal_with_escape_sequences(self):
        source = r'"Line 1\nLine 2\tTabbed\rCarriage Return\\"'
        lexer = Lexer(source)
        expected_token = Token(
            TokenType.STRING_LITERAL, "Line 1\nLine 2\tTabbed\rCarriage Return\\", 1, 1
        )
        token = lexer.read_string_literal()
        self.assertEqual(token, expected_token)

    def test_string_literal_with_invalid_escape_sequence(self):
        source = r'"Invalid escape sequence: \x"'
        lexer = Lexer(source)
        expected_token = Token(
            TokenType.STRING_LITERAL, "Invalid escape sequence: x", 1, 1
        )
        expected_error_message = (
            "Invalid escape sequence: '\\x' is not a valid escape character"
        )
        token = lexer.read_string_literal()
        self.assertEqual(token, expected_token)
        self.assertEqual(len(lexer.collected_errors), 1)
        self.assertEqual(lexer.collected_errors[0].message, expected_error_message)

    def test_ends_with_backslash_at_eof(self):
        source = '"Ends with backslash at EOF: \\'
        lexer = Lexer(source)
        expected_token = Token(
            TokenType.STRING_LITERAL, "Ends with backslash at EOF: ", 1, 1
        )
        expected_error_message = "Unterminated string literal"
        token = lexer.read_string_literal()
        self.assertEqual(token, expected_token)
        self.assertEqual(len(lexer.collected_errors), 2)
        self.assertStartsWith(lexer.collected_errors[0].message, expected_error_message)

    def test_escaped_quote_in_string_literal(self):
        source = r'"She said, \"Hello!\""'
        lexer = Lexer(source)
        expected_token = Token(TokenType.STRING_LITERAL, 'She said, "Hello!"', 1, 1)
        token = lexer.read_string_literal()
        self.assertEqual(token, expected_token)
