from .token import Token, TokenType, KEYWORDS


class FluxLexerError(Exception):
    pass


class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.col = 1
        self.start_col = 1

    def error(self, msg):
        raise FluxLexerError(f"[ligne {self.line}] {msg}")

    def scan_tokens(self):
        while not self._is_at_end():
            self.start = self.current
            self.start_col = self.col
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.col))
        return self.tokens

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        ch = self.source[self.current]
        self.current += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _peek(self):
        return "\0" if self._is_at_end() else self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _match(self, expected):
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self._advance()
        return True

    def _add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line, self.start_col))

    def _scan_token(self):
        ch = self._advance()
        if ch in " \t\r":
            return
        if ch == "\n":
            return

        single_char = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
            "[": TokenType.LEFT_BRACKET,
            "]": TokenType.RIGHT_BRACKET,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
            ";": TokenType.SEMICOLON,
            ":": TokenType.COLON,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "%": TokenType.PERCENT,
            "|": TokenType.PIPE,
            "&": TokenType.AMPERSAND,
        }
        if ch in single_char:
            self._add_token(single_char[ch])
            return

        two_char = {
            ("=", "="): TokenType.EQUAL_EQUAL,
            ("!", "="): TokenType.BANG_EQUAL,
            ("<", "="): TokenType.LESS_EQUAL,
            (">", "="): TokenType.GREATER_EQUAL,
        }
        pair = (ch, self._peek())
        if pair in two_char:
            self._advance()
            self._add_token(two_char[pair])
            return

        if ch == "!":
            self._add_token(TokenType.BANG)
            return
        if ch == "=":
            self._add_token(TokenType.EQUAL)
            return
        if ch == "<":
            self._add_token(TokenType.LESS)
            return
        if ch == ">":
            self._add_token(TokenType.GREATER)
            return
        if ch == "/":
            if self._match("/"):
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            elif self._match("*"):
                depth = 1
                while depth > 0 and not self._is_at_end():
                    if self._peek() == "/" and self._peek_next() == "*":
                        self._advance()
                        self._advance()
                        depth += 1
                    elif self._peek() == "*" and self._peek_next() == "/":
                        self._advance()
                        self._advance()
                        depth -= 1
                    else:
                        self._advance()
            else:
                self._add_token(TokenType.SLASH)
            return

        if ch == '"':
            self._string()
            return

        if ch.isdigit():
            self._number()
            return

        if ch.isalpha() or ch == "_":
            self._identifier()
            return

        self.error(f"caractère inattendu: {ch!r}")

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\\":
                self._advance()
            self._advance()
        if self._is_at_end():
            self.error("chaîne non terminée")
        self._advance()
        raw = self.source[self.start + 1:self.current - 1]
        value = raw.encode().decode("unicode_escape") if "\\" in raw else raw
        self._add_token(TokenType.STRING, value)

    def _number(self):
        while self._peek().isdigit():
            self._advance()
        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
        text = self.source[self.start:self.current]
        self._add_token(TokenType.NUMBER, float(text) if "." in text else int(text))

    def _identifier(self):
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()
        text = self.source[self.start:self.current]
        type_ = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add_token(type_)
