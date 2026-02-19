import unittest
import src.lexer.lexer as lexer

class TestLexerSkipComments(unittest.TestCase):
    
    def test_single_line_comment_skip(self):
        source_code = """// This is a single line comment for testing
int a = 5"""
        lex = lexer.Lexer(source_code)
        
        lex.skip_comment()
        lex.skip_whitespace()  # Skip the newline after comment
        
        # Should now be at 'i' in "int"
        self.assertEqual(lex.current_char, 'i')
        self.assertEqual(lex.line, 2)
        self.assertEqual(lex.column, 1)
    
    def test_multi_line_comment_at_start_skip(self):
        source_code = """/* This is a multi-line comment for testing 
Some more comments
And some more
*/
int a = 5"""
        lex = lexer.Lexer(source_code)
        
        lex.skip_comment()
        lex.skip_whitespace()  # Skip the newline after comment
        
        # Should now be at 'i' in "int"
        self.assertEqual(lex.current_char, 'i')
        self.assertEqual(lex.line, 5)
        self.assertEqual(lex.column, 1)
    
    def test_multi_line_comment_unterminated(self):
        source_code = """/* This is an unterminated multi-line comment for testing 
Some more comments
And some more
int a = 5"""
        lex = lexer.Lexer(source_code)
        
        lex.skip_comment()
        
        # Should have collected an error, not raised exception
        self.assertEqual(len(lex.collected_errors), 1)
        self.assertIn("Unterminated", lex.collected_errors[0].message)
        # Lexer should be at EOF
        self.assertIsNone(lex.current_char)
    
    def test_single_line_comments_inside_multi_line_comment(self):
        source_code = """/* This is a multi-line comment for testing 
// This is a single line comment inside multi-line comment
And some more
*/
int a = 5"""
        lex = lexer.Lexer(source_code)
        
        lex.skip_comment()
        lex.skip_whitespace()
        
        self.assertEqual(lex.current_char, 'i')
        self.assertEqual(lex.line, 5)
        self.assertEqual(lex.column, 1)
    
    def test_multi_line_comments_inside_single_line_comment(self):
        source_code = """// This is a /* multi-line comment inside */ a single line comment for testing
int a = 5"""
        lex = lexer.Lexer(source_code)
        
        lex.skip_comment()
        lex.skip_whitespace()
        
        self.assertEqual(lex.current_char, 'i')
        self.assertEqual(lex.line, 2)
        self.assertEqual(lex.column, 1)
    
    def test_skip_comment_with_no_comments(self):
        source_code = """int a = 5"""
        lex = lexer.Lexer(source_code)
        
        # skip_comment() should do nothing if not at a comment
        lex.skip_comment()
        
        # Should still be at 'i'
        self.assertEqual(lex.current_char, 'i')
        self.assertEqual(lex.line, 1)
        self.assertEqual(lex.column, 1)
    
    def test_single_line_comment_at_eof(self):
        source_code = "// comment with no newline"
        lex = lexer.Lexer(source_code)
        
        lex.skip_comment()
        
        # Should be at EOF
        self.assertIsNone(lex.current_char)
    
    def test_multi_line_comment_on_single_line(self):
        source_code = "/* comment */int a = 5"
        lex = lexer.Lexer(source_code)
        
        lex.skip_comment()
        
        # Should be at 'i' immediately (no newline to skip)
        self.assertEqual(lex.current_char, 'i')
        self.assertEqual(lex.line, 1)
        self.assertEqual(lex.column, 14)