from .parser import parse
from .scope import Identifier
from .tree import CallInlineStatement
from .codegen import CodeGenerator


class Fera:
    @classmethod
    def compiles(self, code, pretty=False):
        program = parse(code)
        codegen = CodeGenerator(program)

        codegen.emit_program()

        compiled = codegen.compile(pretty=False)

        return compiled

    @classmethod
    def compile(self, file, pretty=False):
        return Fera.compiles(file.read(), pretty)