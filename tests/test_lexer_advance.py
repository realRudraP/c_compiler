import unittest
from src.lexer.lexer import Lexer


class TestLexerAdvance(unittest.TestCase):
    def test_advance_moves_position(self):
        lexer = Lexer("abc")

        lexer.advance()

        self.assertEqual(lexer.pos, 1)
        self.assertEqual(lexer.current_char, "b")

    def test_advance_updates_column(self):
        lexer = Lexer("abc")

        lexer.advance()

        self.assertEqual(lexer.column, 2)

    def test_advance_on_newline_updates_line(self):
        lexer = Lexer("a\nb")

        lexer.advance()  # Move to 'a'
        lexer.advance()  # Move to '\n'

        self.assertEqual(lexer.line, 2)
        self.assertEqual(lexer.column, 1)

    def test_advance_at_end_of_source(self):
        lexer = Lexer("a")

        lexer.advance()  # Move to 'a'
        lexer.advance()  # Move past end of source

        self.assertEqual(lexer.pos, 1)
        self.assertIsNone(lexer.current_char)
