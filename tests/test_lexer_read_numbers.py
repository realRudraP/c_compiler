import unittest
from src.lexer.lexer import Lexer
from src.lexer.token import Token, TokenType


class TestLexerReadNumbers(unittest.TestCase):
    def test_read_integer(self):
        lexer = Lexer("123")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.value, "123")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_float(self):
        lexer = Lexer("3.14")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.value, "3.14")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_large_integer(self):
        lexer = Lexer("12345678901234567890")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.value, "12345678901234567890")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_float_with_leading_zero(self):
        lexer = Lexer("0.001")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.value, "0.001")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_float_with_trailing_zero(self):
        lexer = Lexer("1.0")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.value, "1.0")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_float_with_multiple_decimal_points(self):
        lexer = Lexer("1.2.3")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.value, "1.2.3")
        self.assertEqual(len(lexer.collected_errors), 1)
        self.assertIn("multiple decimal points", lexer.collected_errors[0].message)

    def test_read_float_with_decimal_point_at_start(self):
        lexer = Lexer(".5")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.value, ".5")
        self.assertEqual(len(lexer.collected_errors), 1)
        self.assertIn(
            "decimal point cannot be at the start", lexer.collected_errors[0].message
        )

    def test_read_integer_followed_by_identifier(self):
        lexer = Lexer("123abc")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.value, "123")
        self.assertEqual(len(lexer.collected_errors), 1)
        self.assertIn(
            "identifiers cannot start with a digit", lexer.collected_errors[0].message
        )

    def test_read_zero_as_integer(self):
        lexer = Lexer("0")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.value, "0")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_zero_as_float(self):
        lexer = Lexer("0.0")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.value, "0.0")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_negative_integer(self):
        lexer = Lexer("-123")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.value, "-123")
        self.assertEqual(token.line, 1)
        self.assertEqual(token.column, 1)

    def test_read_only_decimal_point(self):
        lexer = Lexer(".")
        token = lexer.read_number()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.value, ".")
        # The two errors are: decimal point cannot be at the start, and decimal point must be followed by digits
        self.assertEqual(len(lexer.collected_errors), 2)
        self.assertIn(
            "decimal point cannot be at the start", lexer.collected_errors[0].message
        )
