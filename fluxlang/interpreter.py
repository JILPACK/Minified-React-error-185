import math
import random
from .token import TokenType
from .ast import (
    Literal, Variable, Assign, Binary, Unary, Logical,
    Grouping, Call, ListExpr, Index,
    ExpressionStmt, PrintStmt, VarStmt, Block,
    IfStmt, WhileStmt, ForStmt, FunStmt, ReturnStmt,
)
from .environment import Environment, FluxFunction, FluxNative, ReturnException


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self._define_natives()

    def _define_natives(self):
        for name, arity, fn in [
            ("clock", 0, lambda: __import__("time").time()),
            ("sqrt", 1, lambda x: math.sqrt(self._to_number(x))),
            ("abs", 1, lambda x: abs(self._to_number(x))),
            ("sin", 1, lambda x: math.sin(self._to_number(x))),
            ("cos", 1, lambda x: math.cos(self._to_number(x))),
            ("tan", 1, lambda x: math.tan(self._to_number(x))),
            ("floor", 1, lambda x: math.floor(self._to_number(x))),
            ("ceil", 1, lambda x: math.ceil(self._to_number(x))),
            ("round", 1, lambda x: round(self._to_number(x))),
            ("rand", 0, lambda: random.random()),
            ("randint", 2, lambda a, b: random.randint(int(self._to_number(a)), int(self._to_number(b)))),
            ("len", 1, lambda x: len(x)),
            ("str", 1, lambda x: str(x)),
            ("num", 1, lambda x: float(x) if "." in str(x) else int(x)),
            ("type", 1, lambda x: type(x).__name__ if hasattr(x, "__name__") else type(x).__name__),
        ]:
            self.globals.define(name, FluxNative(name, arity, fn))

    def interpret(self, statements, trace=False):
        self._trace = trace
        results = []
        for stmt in statements:
            result = self._execute(stmt)
            results.append(result)
        return results

    def _evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value
        if isinstance(expr, Variable):
            return self.environment.get(expr.name)
        if isinstance(expr, Grouping):
            return self._evaluate(expr.expression)
        if isinstance(expr, Unary):
            right = self._evaluate(expr.right)
            if expr.operator.type == TokenType.MINUS:
                return -self._to_number(right)
            if expr.operator.type in (TokenType.BANG, TokenType.NOT):
                return not self._is_truthy(right)
        if isinstance(expr, Binary):
            return self._eval_binary(expr)
        if isinstance(expr, Logical):
            return self._eval_logical(expr)
        if isinstance(expr, Assign):
            value = self._evaluate(expr.value)
            if isinstance(expr.name, Index):
                obj = self._evaluate(expr.name.callee)
                idx = self._evaluate(expr.name.index)
                obj[idx] = value
            else:
                self.environment.assign(expr.name, value)
            return value
        if isinstance(expr, Call):
            return self._eval_call(expr)
        if isinstance(expr, ListExpr):
            return [self._evaluate(e) for e in expr.elements]
        if isinstance(expr, Index):
            obj = self._evaluate(expr.callee)
            idx = self._evaluate(expr.index)
            return obj[idx]
        raise RuntimeError(f"expression inconnue: {type(expr)}")

    def _eval_binary(self, expr):
        left = self._evaluate(expr.left)
        op = expr.operator
        right = self._evaluate(expr.right)

        if op.type == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            raise RuntimeError(f"'+' non supporté entre {type(left).__name__} et {type(right).__name__}")
        if op.type == TokenType.MINUS:
            return self._to_number(left) - self._to_number(right)
        if op.type == TokenType.STAR:
            return self._to_number(left) * self._to_number(right)
        if op.type == TokenType.SLASH:
            r = self._to_number(right)
            if r == 0:
                raise RuntimeError("division par zéro")
            return self._to_number(left) / r
        if op.type == TokenType.PERCENT:
            return self._to_number(left) % self._to_number(right)
        if op.type == TokenType.EQUAL_EQUAL:
            return left == right
        if op.type == TokenType.BANG_EQUAL:
            return left != right
        if op.type == TokenType.LESS:
            return left < right
        if op.type == TokenType.LESS_EQUAL:
            return left <= right
        if op.type == TokenType.GREATER:
            return left > right
        if op.type == TokenType.GREATER_EQUAL:
            return left >= right
        raise RuntimeError(f"opérateur inconnu: {op.lexeme}")

    def _eval_logical(self, expr):
        left = self._evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        elif expr.operator.type == TokenType.AND:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def _eval_call(self, expr):
        callee = self._evaluate(expr.callee)
        args = [self._evaluate(a) for a in expr.arguments]
        if not callable(getattr(callee, 'call', None)):
            raise RuntimeError(f"'{type(callee).__name__}' n'est pas appelable")
        if len(args) != callee.arity():
            raise RuntimeError(f"{callee} attend {callee.arity()} arguments, reçu {len(args)}")
        return callee.call(self, args)

    def _execute(self, stmt):
        if isinstance(stmt, ExpressionStmt):
            return self._evaluate(stmt.expression)
        if isinstance(stmt, PrintStmt):
            value = self._evaluate(stmt.expression)
            self._output(value)
            return
        if isinstance(stmt, VarStmt):
            value = None
            if stmt.initializer:
                value = self._evaluate(stmt.initializer)
            self.environment.define(stmt.name, value)
            return
        if isinstance(stmt, Block):
            self._execute_block(stmt.statements, Environment(self.environment))
            return
        if isinstance(stmt, IfStmt):
            if self._is_truthy(self._evaluate(stmt.condition)):
                return self._execute(stmt.then_branch)
            elif stmt.else_branch:
                return self._execute(stmt.else_branch)
            return
        if isinstance(stmt, WhileStmt):
            while self._is_truthy(self._evaluate(stmt.condition)):
                self._execute(stmt.body)
            return
        if isinstance(stmt, ForStmt):
            iterable = self._evaluate(stmt.iterable)
            for item in iterable:
                self.environment.define(stmt.variable, item)
                self._execute(stmt.body)
            return
        if isinstance(stmt, FunStmt):
            fun = FluxFunction(stmt, self.environment)
            self.environment.define(stmt.name, fun)
            return
        if isinstance(stmt, ReturnStmt):
            value = None
            if stmt.value:
                value = self._evaluate(stmt.value)
            raise ReturnException(value)
        raise RuntimeError(f"instruction inconnue: {type(stmt)}")

    def _execute_block(self, statements, env):
        previous = self.environment
        try:
            self.environment = env
            for stmt in statements:
                self._execute(stmt)
        finally:
            self.environment = previous

    def _is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def _to_number(self, value):
        if isinstance(value, (int, float)):
            if isinstance(value, bool):
                return float(value)
            return value
        try:
            return float(value)
        except (TypeError, ValueError):
            raise RuntimeError(f"valeur numérique attendue, reçu {type(value).__name__}")

    def _output(self, value):
        import sys
        if value is None:
            print("nil")
        elif isinstance(value, bool):
            print("true" if value else "false")
        elif isinstance(value, float):
            s = f"{value:.10f}".rstrip("0").rstrip(".")
            print(s)
        elif isinstance(value, list):
            print("[" + ", ".join(str(v) for v in value) + "]")
        else:
            print(value)
