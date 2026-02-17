import unittest
import src.lexer.lexer as lexer


class TestLexerSkipComments(unittest.TestCase):
    def test_single_line_comment_skip(self):
        source_code = """// This is a single line comment for testing
        int a = 5
        int b = 10
        """
        lex = lexer.Lexer(source_code)
        while lex.current_char is not None and lex.current_char.isspace():
            lex.advance()
        lex.skip_comment()
        self.assertEqual(lex.line, 2)
        self.assertEqual(lex.column, 1)

    def test_multi_line_comment_at_start_skip(self):
        source_code = """/* This is a multi-line comment for testing 
        Some more comments
        And some more
        */
        int a = 5
        int b = 10
        """
        lex = lexer.Lexer(source_code)
        while lex.current_char is not None and lex.current_char.isspace():
            lex.advance()
        lex.skip_comment()
        self.assertEqual(lex.line, 5)
        self.assertEqual(lex.column, 1)

    def test_multi_line_comment_unterminated(self):
        source_code = """/* This is an unterminated multi-line comment for testing 
        Some more comments
        And some more
        int a = 5
        int b = 10
        """
        lex = lexer.Lexer(source_code)
        while lex.current_char is not None and lex.current_char.isspace():
            lex.advance()
        with self.assertRaises(Exception) as context:
            lex.skip_comment()
        self.assertIn("Unterminated comment", str(context.exception))

    def test_single_line_comments_inside_multi_line_comment(self):
        source_code = """/* This is a multi-line comment for testing 
        // This is a single line comment inside multi-line comment
        And some more
        */
        int a = 5
        int b = 10
        """
        lex = lexer.Lexer(source_code)
        while lex.current_char is not None and lex.current_char.isspace():
            lex.advance()
        lex.skip_comment()
        self.assertEqual(lex.line, 5)
        self.assertEqual(lex.column, 1)

    def test_multi_line_comments_inside_single_line_comment(self):
        source_code = """// This is a /* multi-line comment inside */ a single line comment for testing
        int a = 5
        int b = 10
        """
        lex = lexer.Lexer(source_code)
        while lex.current_char is not None and lex.current_char.isspace():
            lex.advance()
        lex.skip_comment()
        self.assertEqual(lex.line, 2)
        self.assertEqual(lex.column, 1)
    
    def test_skip_comment_with_no_comments(self):
        source_code = """int a = 5
        int b = 10
        """
        lex = lexer.Lexer(source_code)
        while lex.current_char is not None and lex.current_char.isspace():
            lex.advance()
        lex.skip_comment()
        self.assertEqual(lex.line, 1)
        self.assertEqual(lex.column, 1)

# TODO: Add tests for comments that appear after some code on the same line, and ensure that the lexer correctly skips the comment and continues processing the code.