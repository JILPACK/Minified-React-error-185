from .token import TokenType


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(f"variable non définie: {name}")

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(f"variable non définie: {name}")


class FluxFunction:
    def __init__(self, declaration, closure, is_initializer=False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        env = Environment(self.closure)
        for name, value in zip(self.declaration.params, arguments):
            env.define(name, value)
        try:
            interpreter._execute_block(self.declaration.body, env)
        except ReturnException as ret:
            return ret.value
        return None

    def __repr__(self):
        return f"<fn {self.declaration.name}>"


class FluxNative:
    def __init__(self, name, arity, fn):
        self._name = name
        self._arity = arity
        self._fn = fn

    def arity(self):
        return self._arity

    def call(self, interpreter, arguments):
        return self._fn(*arguments)

    def __repr__(self):
        return f"<native {self._name}>"
