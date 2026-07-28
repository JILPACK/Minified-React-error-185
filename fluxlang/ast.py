"""AST node definitions for FluxLang."""


class Expr:
    pass


class Stmt:
    pass


# --- Expressions ---

class Literal(Expr):
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value!r})"


class Variable(Expr):
    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"


class Assign(Expr):
    __slots__ = ("name", "value")

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assign({self.name}, {self.value})"


class Binary(Expr):
    __slots__ = ("left", "operator", "right")

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Binary({self.left} {self.operator.lexeme} {self.right})"


class Unary(Expr):
    __slots__ = ("operator", "right")

    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Unary({self.operator.lexeme} {self.right})"


class Logical(Expr):
    __slots__ = ("left", "operator", "right")

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Logical({self.left} {self.operator.lexeme} {self.right})"


class Grouping(Expr):
    __slots__ = ("expression",)

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Group({self.expression})"


class Call(Expr):
    __slots__ = ("callee", "paren", "arguments")

    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def __repr__(self):
        return f"Call({self.callee}, {self.arguments})"


class ListExpr(Expr):
    __slots__ = ("elements",)

    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"List({self.elements})"


class Index(Expr):
    __slots__ = ("callee", "index")

    def __init__(self, callee, index):
        self.callee = callee
        self.index = index

    def __repr__(self):
        return f"Index({self.callee}[{self.index}])"


# --- Statements ---

class ExpressionStmt(Stmt):
    __slots__ = ("expression",)

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"ExprStmt({self.expression})"


class PrintStmt(Stmt):
    __slots__ = ("expression",)

    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"Print({self.expression})"


class VarStmt(Stmt):
    __slots__ = ("name", "initializer")

    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def __repr__(self):
        return f"Var({self.name}, {self.initializer})"


class Block(Stmt):
    __slots__ = ("statements",)

    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({len(self.statements)} stmts)"


class IfStmt(Stmt):
    __slots__ = ("condition", "then_branch", "else_branch")

    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"If({self.condition})"


class WhileStmt(Stmt):
    __slots__ = ("condition", "body")

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition})"


class ForStmt(Stmt):
    __slots__ = ("variable", "iterable", "body")

    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body


class FunStmt(Stmt):
    __slots__ = ("name", "params", "body")

    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"Fun({self.name}, {self.params})"


class ReturnStmt(Stmt):
    __slots__ = ("keyword", "value")

    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"
