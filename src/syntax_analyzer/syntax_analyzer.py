from src.lexer.lexer import Lexer
from src.lexer.token_types import TokenType
from src.error.syntactical import SyntacticalError


class SyntaxAnalyzer:
    def __init__(self, source_code: str):
        self.lexer = Lexer(source_code)
        self.current_token = None
        self.peek_token = None
        self.errors = []
        self.paren_stack = []  # Stack to track open parens/brackets
        self.advance()  # Initialize current_token

    def advance(self):
        """Move to next token"""
        self.current_token = self.peek_token or self.lexer.get_next_token()
        self.peek_token = self.lexer.get_next_token()

    def expect(self, token_type: TokenType) -> bool:
        """Check if current token matches expected type"""
        if self.current_token.type == token_type:
            self.advance()
            return True
        else:
            self.errors.append(
                SyntacticalError(
                    f"Expected {token_type}, got {self.current_token.type}",
                    self.current_token.line,
                    self.current_token.column,
                )
            )
            return False

    def track_opening_bracket(self, token_type: TokenType):
        """Track opening brackets/parens"""
        self.paren_stack.append((token_type, self.current_token.line, self.current_token.column))

    def track_closing_bracket(self, token_type: TokenType) -> bool:
        """Track closing brackets/parens and validate matching"""
        if not self.paren_stack:
            self.errors.append(
                SyntacticalError(
                    f"Unexpected closing '{self.current_token.value}' with no matching opening bracket",
                    self.current_token.line,
                    self.current_token.column,
                )
            )
            return False

        opening_type, opening_line, opening_col = self.paren_stack[-1]

        # Map closing to opening
        closing_map = {
            TokenType.RIGHT_PARAN: TokenType.LEFT_PARAN,
            TokenType.RIGHT_BRACE: TokenType.LEFT_BRACE,
            TokenType.RIGHT_BRACKET: TokenType.LEFT_BRACKET,
        }

        if closing_map[token_type] != opening_type:
            self.errors.append(
                SyntacticalError(
                    f"Mismatched bracket: '{self.current_token.value}' does not match opening bracket at line {opening_line}, col {opening_col}",
                    self.current_token.line,
                    self.current_token.column,
                )
            )
            # Still pop to avoid cascading errors
            self.paren_stack.pop()
            return False

        self.paren_stack.pop()
        return True

    # Parse methods for each loop type

    def parse_for_loop(self) -> bool:
        """
        for (init; condition; increment) { body }
        """
        if not self.expect(TokenType.FOR):
            return False

        if not self.expect(TokenType.LEFT_PARAN):
            return False
        self.track_opening_bracket(TokenType.LEFT_PARAN)

        # Parse initialization (can be declaration or expression)
        self.parse_expression()

        self.expect(TokenType.SEMICOLON)

        # Parse condition
        self.parse_expression()

        self.expect(TokenType.SEMICOLON)

        # Parse increment
        self.parse_expression()

        self.expect(TokenType.RIGHT_PARAN)
        self.track_closing_bracket(TokenType.RIGHT_PARAN)

        # Parse body (can be block or single statement)
        self.parse_statement()

        return True

    def parse_while_loop(self) -> bool:
        """
        while (condition) { body }
        """
        if not self.expect(TokenType.WHILE):
            return False

        if not self.expect(TokenType.LEFT_PARAN):
            return False
        self.track_opening_bracket(TokenType.LEFT_PARAN)

        self.parse_expression()

        self.expect(TokenType.RIGHT_PARAN)
        self.track_closing_bracket(TokenType.RIGHT_PARAN)

        self.parse_statement()

        return True

    def parse_do_while_loop(self) -> bool:
        """
        do { body } while (condition);
        """
        if not self.expect(TokenType.DO):
            return False

        self.parse_statement()

        if not self.expect(TokenType.WHILE):
            return False

        if not self.expect(TokenType.LEFT_PARAN):
            return False
        self.track_opening_bracket(TokenType.LEFT_PARAN)

        self.parse_expression()

        if not self.expect(TokenType.RIGHT_PARAN):
            return False
        self.track_closing_bracket(TokenType.RIGHT_PARAN)

        # Require semicolon after do-while
        if self.current_token.type != TokenType.SEMICOLON:
            self.errors.append(
                SyntacticalError(
                    f"Expected ';' after do-while statement, got {self.current_token.type}",
                    self.current_token.line,
                    self.current_token.column,
                )
            )
        else:
            self.expect(TokenType.SEMICOLON)

        return True

    def parse_if_statement(self) -> bool:
        """
        if (condition) statement [else statement]
        """
        if not self.expect(TokenType.IF):
            return False

        if not self.expect(TokenType.LEFT_PARAN):
            return False
        self.track_opening_bracket(TokenType.LEFT_PARAN)

        self.parse_expression()

        if not self.expect(TokenType.RIGHT_PARAN):
            return False
        self.track_closing_bracket(TokenType.RIGHT_PARAN)

        # Parse the if body (can be block or statement)
        self.parse_statement()

        # Handle optional else
        if self.current_token.type == TokenType.ELSE:
            self.expect(TokenType.ELSE)
            self.parse_statement()

        return True

    def parse_statement(self):
        """
        Handle nested loops and blocks
        A statement can be:
        - A block
        - A loop: for, while, do-while
        - An if/else statement (skip over it)
        - A simple statement: single token followed by semicolon or other terminator
        """
        if self.current_token.type == TokenType.LEFT_BRACE:
            self.expect(TokenType.LEFT_BRACE)
            self.track_opening_bracket(TokenType.LEFT_BRACE)

            while (
                self.current_token.type != TokenType.RIGHT_BRACE
                and self.current_token.type != TokenType.EOF
            ):
                if self.current_token.type == TokenType.FOR:
                    self.parse_for_loop()
                elif self.current_token.type == TokenType.WHILE:
                    self.parse_while_loop()
                elif self.current_token.type == TokenType.DO:
                    self.parse_do_while_loop()
                elif self.current_token.type == TokenType.IF:
                    self.parse_if_statement()
                else:
                    # Track brackets in other statements
                    if self.current_token.type in [
                        TokenType.LEFT_PARAN,
                        TokenType.LEFT_BRACKET,
                    ]:
                        self.track_opening_bracket(self.current_token.type)
                    elif self.current_token.type in [
                        TokenType.RIGHT_PARAN,
                        TokenType.RIGHT_BRACKET,
                    ]:
                        self.track_closing_bracket(self.current_token.type)

                    self.advance()

            if self.current_token.type == TokenType.RIGHT_BRACE:
                self.expect(TokenType.RIGHT_BRACE)
                self.track_closing_bracket(TokenType.RIGHT_BRACE)
            else:
                self.errors.append(
                    SyntacticalError(
                        f"Expected closing brace '}}' but got {self.current_token.type}",
                        self.current_token.line,
                        self.current_token.column,
                    )
                )
        elif self.current_token.type == TokenType.FOR:
            self.parse_for_loop()
        elif self.current_token.type == TokenType.WHILE:
            self.parse_while_loop()
        elif self.current_token.type == TokenType.DO:
            self.parse_do_while_loop()
        elif self.current_token.type == TokenType.IF:
            self.parse_if_statement()
        else:
            # Single statement (not a block or loop)
            # Check if it's a parenthesized statement (invalid as loop body)
            if self.current_token.type == TokenType.LEFT_PARAN:
                self.errors.append(
                    SyntacticalError(
                        f"Invalid statement: parenthesized statements cannot be used as loop body. Use braces instead: {{ ... }}",
                        self.current_token.line,
                        self.current_token.column,
                    )
                )
                # Still track it to avoid cascading errors
                self.track_opening_bracket(self.current_token.type)
            elif self.current_token.type in [TokenType.LEFT_BRACKET]:
                self.track_opening_bracket(self.current_token.type)
            elif self.current_token.type in [TokenType.RIGHT_PARAN, TokenType.RIGHT_BRACKET]:
                self.track_closing_bracket(self.current_token.type)

            self.advance()

    def parse_expression(self):
        """
        Parse expressions and track brackets within them
        """
        paren_depth = 0
        bracket_depth = 0
        
        while self.current_token.type != TokenType.EOF:
            # Stop at delimiters only if we're not inside nested brackets
            if paren_depth == 0 and bracket_depth == 0:
                if self.current_token.type in [
                    TokenType.SEMICOLON,
                    TokenType.RIGHT_PARAN,
                    TokenType.RIGHT_BRACE,
                ]:
                    break
            
            if self.current_token.type == TokenType.LEFT_PARAN:
                self.track_opening_bracket(self.current_token.type)
                paren_depth += 1
            elif self.current_token.type == TokenType.RIGHT_PARAN:
                self.track_closing_bracket(self.current_token.type)
                paren_depth = max(0, paren_depth - 1)
            elif self.current_token.type == TokenType.LEFT_BRACKET:
                self.track_opening_bracket(self.current_token.type)
                bracket_depth += 1
            elif self.current_token.type == TokenType.RIGHT_BRACKET:
                self.track_closing_bracket(self.current_token.type)
                bracket_depth = max(0, bracket_depth - 1)

            self.advance()

    def check_unclosed_brackets(self):
        """Check if all brackets were closed"""
        if self.paren_stack:
            for bracket_type, line, col in self.paren_stack:
                bracket_map = {
                    TokenType.LEFT_PARAN: "(",
                    TokenType.LEFT_BRACE: "{",
                    TokenType.LEFT_BRACKET: "[",
                }
                self.errors.append(
                    SyntacticalError(
                        f"Unclosed '{bracket_map[bracket_type]}' starting at line {line}, column {col}",
                        line,
                        col,
                    )
                )

    def analyze(self) -> bool:
        """Main entry point - returns True only if no errors were collected"""
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.FOR:
                self.parse_for_loop()
            elif self.current_token.type == TokenType.WHILE:
                self.parse_while_loop()
            elif self.current_token.type == TokenType.DO:
                self.parse_do_while_loop()
            elif self.current_token.type in [TokenType.LEFT_PARAN, TokenType.LEFT_BRACKET]:
                # Track brackets in top-level statements
                self.track_opening_bracket(self.current_token.type)
                self.advance()
            elif self.current_token.type in [TokenType.RIGHT_PARAN, TokenType.RIGHT_BRACKET, TokenType.RIGHT_BRACE]:
                # Detect stray closing brackets
                self.track_closing_bracket(self.current_token.type)
                self.advance()
            else:
                self.advance()

        # Final check for unclosed brackets
        self.check_unclosed_brackets()

        return len(self.errors) == 0

    def get_errors(self):
        """Return all collected errors"""
        return self.errors