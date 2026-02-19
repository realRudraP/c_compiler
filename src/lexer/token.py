from dataclasses import dataclass
from .token_types import TokenType


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, column={self.column})"

    def __str__(self):
        return f"{self.type.name}({self.value})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (
            self.type == other.type
            and self.value == other.value
            and self.line == other.line
            and self.column == other.column
        )
