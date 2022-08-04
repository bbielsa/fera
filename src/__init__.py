from parser import parse
from scope import Identifier
from tree import CallInlineStatement
from codegen import CodeGenerator

code = '''
    data {
        a: byte = 0;
        b: byte = 1;
        c: byte = 0;
        t0: byte;
        t1: byte;
    }

    inline _dadd {
        __org($0)
        [
            __rel($0, $1) +
            __rel($1, $0) -
        ]
        __ret($0)
    }

    inline _cpy {
        __org($2) [-]
        __rel($2, $0)
        [
            __rel($0, $1) +
            __rel($1, $2) +
            __rel($2, $0) -
        ]
        __rel($0, $2)
        [
            __rel($2, $0) +
            __rel($0, $2) -
        ]
        __ret($2)
    }

    inline _clr {
        __org($0) [-]
        __ret($0)
    }

    entry {
        for i = 0...7 {
            _cpy(b, c, t0);
            _clr(t0);
            _cpy(a, t0, t1);
            _clr(t1);
            _dadd(a, b);
            _cpy(t0, a, t1);
            _clr(t1);
            _clr(t0);
            _cpy(c, b, t0);
            _clr(t0);
        }
    }
'''

program = parse(code)
# print(program.data_block.body[1].constant[2].value)
codegen = CodeGenerator(program)
codegen.emit_program()
compiled = codegen.compile(pretty=False)

print(compiled)