"""FluxLang REPL - Lancer avec : python -m fluxlang"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fluxlang.lexer import Lexer, FluxLexerError
from fluxlang.parser import Parser, ParseError
from fluxlang.interpreter import Interpreter


def main():
    print("FluxLang v1.0 - REPL interactif")
    print("Tapez 'exit' pour quitter, 'clear' pour effacer")
    print()

    interp = Interpreter()
    context = ""

    while True:
        try:
            if context:
                line = input("... ")
            else:
                line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir!")
            break

        if line.strip() == "exit":
            break
        if line.strip() == "clear":
            context = ""
            continue

        context += line + "\n"

        try:
            lexer = Lexer(context)
            tokens = lexer.scan_tokens()
            parser = Parser(tokens)
            ast = parser.parse()
            interp.interpret(ast)
            context = ""
        except (FluxLexerError, ParseError, SyntaxError) as e:
            if not context.endswith("}\n") and not context.endswith(";\n"):
                continue
            print(f"  ⚠ {e}")
            context = ""
        except Exception as e:
            print(f"  ⚠ {e}")
            context = ""


if __name__ == "__main__":
    main()
