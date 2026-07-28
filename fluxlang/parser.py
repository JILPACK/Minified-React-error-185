from .token import TokenType
from .ast import (
    Expr, Stmt,
    Literal, Variable, Assign, Binary, Unary, Logical,
    Grouping, Call, ListExpr, Index,
    ExpressionStmt, PrintStmt, VarStmt, Block,
    IfStmt, WhileStmt, ForStmt, FunStmt, ReturnStmt,
)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self._is_at_end():
            stmt = self._declaration()
            if stmt:
                statements.append(stmt)
        return statements

    def _declaration(self):
        try:
            if self._match(TokenType.LET):
                return self._var_declaration()
            if self._match(TokenType.FUN):
                return self._function()
            if self._match(TokenType.IMPORT):
                return self._import_stmt()
            return self._statement()
        except ParseError:
            self._synchronize()
            return None

    def _var_declaration(self):
        name = self._consume(TokenType.IDENTIFIER, "nom de variable attendu")
        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "attendu ';' après la déclaration")
        return VarStmt(name.lexeme, initializer)

    def _function(self):
        name = self._consume(TokenType.IDENTIFIER, "nom de fonction attendu")
        self._consume(TokenType.LEFT_PAREN, "attendu '(' après le nom")
        params = []
        if not self._check(TokenType.RIGHT_PAREN):
            params.append(self._consume(TokenType.IDENTIFIER, "nom de paramètre attendu").lexeme)
            while self._match(TokenType.COMMA):
                params.append(self._consume(TokenType.IDENTIFIER, "nom de paramètre attendu").lexeme)
        self._consume(TokenType.RIGHT_PAREN, "attendu ')' après les paramètres")
        self._consume(TokenType.LEFT_BRACE, "attendu '{' avant le corps")
        body = self._block()
        return FunStmt(name.lexeme, params, body)

    def _import_stmt(self):
        self._consume(TokenType.STRING, "chemin de module attendu")
        self._consume(TokenType.SEMICOLON, "; attendu")
        return ExpressionStmt(Literal(None))

    def _statement(self):
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.FOR):
            return self._for_statement()
        if self._match(TokenType.RETURN):
            return self._return_statement()
        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())
        return self._expression_statement()

    def _print_statement(self):
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "attendu ';' après la valeur")
        return PrintStmt(value)

    def _if_statement(self):
        if self._check(TokenType.LEFT_PAREN):
            self._advance()
            condition = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "attendu ')'")
        else:
            condition = self._expression()
        then_branch = self._statement()
        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()
        return IfStmt(condition, then_branch, else_branch)

    def _while_statement(self):
        if self._check(TokenType.LEFT_PAREN):
            self._advance()
            condition = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "attendu ')'")
        else:
            condition = self._expression()
        body = self._statement()
        return WhileStmt(condition, body)

    def _for_statement(self):
        if self._match(TokenType.LEFT_PAREN):
            if self._match(TokenType.LET):
                initializer = self._var_declaration()
            elif self._match(TokenType.SEMICOLON):
                initializer = None
            else:
                initializer = ExpressionStmt(self._expression())
                self._consume(TokenType.SEMICOLON, "; attendu")
            condition = None
            if not self._check(TokenType.SEMICOLON):
                condition = self._expression()
            self._consume(TokenType.SEMICOLON, "; attendu")
            increment = None
            if not self._check(TokenType.RIGHT_PAREN):
                increment = self._expression()
            self._consume(TokenType.RIGHT_PAREN, ") attendu")
            body = self._statement()
            if increment:
                body = Block([body, ExpressionStmt(increment)])
            condition = condition or Literal(True)
            body = WhileStmt(condition, body)
            if initializer:
                body = Block([initializer, body])
            return body
        else:
            if self._match(TokenType.LET):
                var_name = self._consume(TokenType.IDENTIFIER, "nom de variable")
                self._consume(TokenType.IN, "'in' attendu")
                iterable = self._expression()
                body = self._statement()
                return ForStmt(var_name.lexeme, iterable, body)
            raise ParseError(self._error(self._peek(), "attendu '(' ou 'let' après 'for'"))

    def _return_statement(self):
        keyword = self._previous()
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        self._consume(TokenType.SEMICOLON, "; attendu")
        return ReturnStmt(keyword, value)

    def _block(self):
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            stmt = self._declaration()
            if stmt:
                statements.append(stmt)
        self._consume(TokenType.RIGHT_BRACE, "attendu '}'")
        return statements

    def _expression_statement(self):
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "attendu ';' après l'expression")
        return ExpressionStmt(expr)

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        expr = self._or()
        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()
            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            elif isinstance(expr, Index):
                return Assign(expr, value)
            raise ParseError(self._error(equals, "cible d'affectation invalide"))
        return expr

    def _or(self):
        expr = self._and()
        while self._match(TokenType.OR):
            operator = self._previous()
            right = self._and()
            expr = Logical(expr, operator, right)
        return expr

    def _and(self):
        expr = self._equality()
        while self._match(TokenType.AND):
            operator = self._previous()
            right = self._equality()
            expr = Logical(expr, operator, right)
        return expr

    def _equality(self):
        expr = self._comparison()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _factor(self):
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)
        return expr

    def _unary(self):
        if self._match(TokenType.MINUS, TokenType.BANG, TokenType.NOT):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        return self._call()

    def _call(self):
        expr = self._primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            elif self._match(TokenType.LEFT_BRACKET):
                index = self._expression()
                self._consume(TokenType.RIGHT_BRACKET, "] attendu")
                expr = Index(expr, index)
            else:
                break
        return expr

    def _finish_call(self, callee):
        arguments = []
        if not self._check(TokenType.RIGHT_PAREN):
            arguments.append(self._expression())
            while self._match(TokenType.COMMA):
                arguments.append(self._expression())
        paren = self._consume(TokenType.RIGHT_PAREN, "')' attendu")
        return Call(callee, paren, arguments)

    def _primary(self):
        if self._match(TokenType.NUMBER):
            return Literal(self._previous().literal)
        if self._match(TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.NIL):
            return Literal(None)
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous().lexeme)
        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "')' attendu")
            return Grouping(expr)
        if self._match(TokenType.LEFT_BRACKET):
            elements = []
            if not self._check(TokenType.RIGHT_BRACKET):
                elements.append(self._expression())
                while self._match(TokenType.COMMA):
                    elements.append(self._expression())
            self._consume(TokenType.RIGHT_BRACKET, "']' attendu")
            return ListExpr(elements)
        raise ParseError(self._error(self._peek(), "expression attendue"))

    # --- Helpers ---

    def _match(self, *types):
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _check(self, type_):
        if self._is_at_end():
            return False
        return self._peek().type == type_

    def _advance(self):
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _consume(self, type_, msg):
        if self._check(type_):
            return self._advance()
        raise ParseError(self._error(self._peek(), msg))

    def _error(self, token, msg):
        return f"[ligne {token.line}] Erreur: {msg}"

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            if self._peek().type in (TokenType.LET, TokenType.FUN, TokenType.IF, TokenType.WHILE, TokenType.FOR, TokenType.RETURN, TokenType.PRINT):
                return
            self._advance()
