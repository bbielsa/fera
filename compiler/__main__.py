from .parser import parse
from .scope import Identifier
from .tree import CallInlineStatement
from .codegen import CodeGenerator

code = '''
    data {
        x: byte = 104;
        r: byte;
        z: byte[100];
        nl: byte = 10;
    }

    inline _putc {
        __org($0)
        .
        __ret($0)
    }

    entry {
        r = x;
        _putc(x);
        r = r + 1;
        _putc(r);
        _putc(nl);
    }
'''

program = parse(code)
codegen = CodeGenerator(program)

codegen.emit_program()

compiled = codegen.compile(pretty=False)

print(compiled)
