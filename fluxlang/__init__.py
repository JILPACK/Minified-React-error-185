from .lexer import Lexer, FluxLexerError
from .parser import Parser, ParseError
from .interpreter import Interpreter
from .environment import FluxFunction, FluxNative


def run(source, output_func=None):
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    interp = Interpreter()
    if output_func:
        original_print = interp._output
        interp._output = output_func
    results = interp.interpret(ast)
    return results


def run_source(source):
    lines = []
    def capture(value):
        lines.append(value)
    run(source, capture)
    return "\n".join(str(l) for l in lines)
