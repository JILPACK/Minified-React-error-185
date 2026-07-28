from enum import auto, Enum


class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    DOT = auto()
    SEMICOLON = auto()
    COLON = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    PIPE = auto()
    AMPERSAND = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    LET = auto()
    FUN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IN = auto()
    IMPORT = auto()

    EOF = auto()


KEYWORDS = {
    "let": TokenType.LET,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "return": TokenType.RETURN,
    "print": TokenType.PRINT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "nil": TokenType.NIL,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "in": TokenType.IN,
    "import": TokenType.IMPORT,
}


class Token:
    __slots__ = ("type", "lexeme", "literal", "line", "col")

    def __init__(self, type_, lexeme, literal, line, col):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme!r})"
