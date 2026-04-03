import unittest
from src.syntax_analyzer.syntax_analyzer import SyntaxAnalyzer


class TestSyntaxAnalyzerBasicLoops(unittest.TestCase):
    """Test basic loop structures"""

    def test_simple_for_loop(self):
        code = "for (int i = 0; i < 10; i++) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_simple_while_loop(self):
        code = "while (x > 0) { x--; }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_simple_do_while_loop(self):
        code = "do { x++; } while (x < 10);"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_for_loop_without_braces(self):
        code = "for (int i = 0; i < 10; i++) x++;"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_while_loop_without_braces(self):
        code = "while (x > 0) x--;"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)


class TestSyntaxAnalyzerNestedLoops(unittest.TestCase):
    """Test nested loop structures"""

    def test_nested_for_loops(self):
        code = """
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                x++;
            }
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_nested_while_loops(self):
        code = """
        while (x > 0) {
            while (y > 0) {
                y--;
            }
            x--;
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_for_inside_while(self):
        code = """
        while (x > 0) {
            for (int i = 0; i < 5; i++) {
                x--;
            }
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_while_inside_for(self):
        code = """
        for (int i = 0; i < 10; i++) {
            while (x > 0) {
                x--;
            }
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_do_while_inside_for(self):
        code = """
        for (int i = 0; i < 10; i++) {
            do {
                x++;
            } while (x < 5);
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_deeply_nested_loops(self):
        code = """
        for (int i = 0; i < 10; i++) {
            while (x > 0) {
                for (int j = 0; j < 5; j++) {
                    do {
                        y++;
                    } while (y < 10);
                }
            }
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)


class TestSyntaxAnalyzerMissingBrackets(unittest.TestCase):
    """Test detection of missing/mismatched brackets"""

    def test_missing_closing_paren_in_for(self):
        code = "for (int i = 0; i < 10; i++ { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)

    def test_missing_closing_brace(self):
        code = "for (int i = 0; i < 10; i++) { x++;"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)

    def test_missing_opening_paren_in_while(self):
        code = "while x > 0) { x--; }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)

    def test_missing_opening_brace(self):
        code = "for (int i = 0; i < 10; i++) x++; }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)
        # Should have error about unexpected closing brace
        error_messages = [e.message for e in analyzer.get_errors()]
        self.assertTrue(any("Unexpected closing" in msg for msg in error_messages))

    def test_extra_closing_brace(self):
        code = "for (int i = 0; i < 10; i++) { } }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)
        # Should have error about unexpected closing brace
        error_messages = [e.message for e in analyzer.get_errors()]
        self.assertTrue(any("Unexpected closing" in msg for msg in error_messages))

    def test_extra_closing_paren(self):
        code = "while (x > 0)) { x--; }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)


class TestSyntaxAnalyzerMismatchedBrackets(unittest.TestCase):
    """Test detection of mismatched brackets"""

    def test_bracket_instead_of_paren_in_for(self):
        code = "for [int i = 0; i < 10; i++) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)

    def test_paren_instead_of_brace(self):
        code = "for (int i = 0; i < 10; i++) ( x++; )"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)
        # Should have error about unexpected closing paren
        error_messages = [e.message for e in analyzer.get_errors()]
        self.assertTrue(any("parenthesized statements" in msg.lower() for msg in error_messages))

    def test_brace_instead_of_paren_in_while(self):
        code = "while { x > 0 } { x--; }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)


class TestSyntaxAnalyzerMissingSyntaxElements(unittest.TestCase):
    """Test detection of missing syntax elements"""

    def test_for_loop_missing_semicolon_after_init(self):
        code = "for (int i = 0 i < 10; i++) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)

    def test_for_loop_missing_semicolon_after_condition(self):
        code = "for (int i = 0; i < 10 i++) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)

    def test_do_while_missing_semicolon_at_end(self):
        code = "do { x++; } while (x < 10)"
        analyzer = SyntaxAnalyzer(code)
        # Missing semicolon after condition - technically should fail
        # But our basic analyzer doesn't strictly enforce this
        # Adjust based on your requirements
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)

    def test_for_loop_missing_init(self):
        code = "for (; i < 10; i++) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())  # Valid: init can be empty
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_for_loop_missing_condition(self):
        code = "for (int i = 0; ; i++) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())  # Valid: condition can be empty
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_for_loop_missing_increment(self):
        code = "for (int i = 0; i < 10; ) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())  # Valid: increment can be empty
        self.assertEqual(len(analyzer.get_errors()), 0)


class TestSyntaxAnalyzerComplexNesting(unittest.TestCase):
    """Test complex nesting scenarios"""

    def test_multiple_statements_per_loop(self):
        code = """
        for (int i = 0; i < 10; i++) {
            x++;
            y--;
            z = x + y;
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_multiple_nested_loops_at_same_level(self):
        code = """
        for (int i = 0; i < 10; i++) {
            x++;
        }
        while (y > 0) {
            y--;
        }
        do {
            z++;
        } while (z < 5);
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_loop_with_array_access(self):
        code = """
        for (int i = 0; i < 10; i++) {
            arr[i] = i;
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_loop_with_function_call(self):
        code = """
        for (int i = 0; i < 10; i++) {
            func(i, arr[i]);
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_deeply_nested_with_multiple_statements(self):
        code = """
        for (int i = 0; i < 10; i++) {
            x++;
            while (y > 0) {
                y--;
                z = func(x[i], y);
                if (z > 10) {
                    do {
                        z--;
                    } while (z > 0);
                }
            }
            x--;
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)


class TestSyntaxAnalyzerEdgeCases(unittest.TestCase):
    """Test edge cases"""

    def test_empty_for_loop(self):
        code = "for (;;) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_empty_while_loop(self):
        code = "while (1) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_loop_with_complex_condition(self):
        code = "while ((a && b) || (c < d)) { }"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_loop_with_nested_parens_in_condition(self):
        code = "for (int i = 0; (i < 10) && (i > -1); i++) { }"
        analyzer = SyntaxAnalyzer(code)
        # This should pass - nested parens in condition are valid
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)

    def test_single_line_nested_loops(self):
        code = "for(int i=0;i<5;i++){while(j>0){j--;}}"
        analyzer = SyntaxAnalyzer(code)
        self.assertTrue(analyzer.analyze())
        self.assertEqual(len(analyzer.get_errors()), 0)


class TestSyntaxAnalyzerMultipleErrors(unittest.TestCase):
    """Test handling of multiple errors in one pass"""

    def test_multiple_bracket_errors(self):
        code = """
        for (int i = 0; i < 10; i++ {
            while (x > 0 {
                x--;
        }
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 1)

    def test_mixed_bracket_and_syntax_errors(self):
        code = """
        for (int i = 0 i < 10; i++) {
            while (y > 0) x--;
        """
        analyzer = SyntaxAnalyzer(code)
        self.assertFalse(analyzer.analyze())
        self.assertGreater(len(analyzer.get_errors()), 0)


if __name__ == "__main__":
    unittest.main()