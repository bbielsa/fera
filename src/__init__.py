from parser import parse
from scope import Identifier
from tree import CallInlineStatement
from codegen import CodeGenerator

code = '''
    data {
        x: byte = 255;
        y: byte = 69;
    }

    inline _clr {
        __org($0)
        [-]
        __ret($0)
    }

    entry {
    }
'''

add = '''
    data {
        x: byte = 45;
        y: byte = 200;
    }

    inline _dadd {
        __org($0)
        [
        __rel($0, $1) +
        __rel($1, $0) -
        ]
        __ret($0)
    }

    entry {
    }
'''

'''
    Notes:
        - Loop 1 moves i to blank space of array
        - Loop 2 restores i

'''

arr = '''
    data {
        res: byte = 0;
        i: byte = 0;

        arr: byte = 0;
        r: byte = 0;
        w: byte = 0;
        d: byte = 0;

        a1: byte = 104;
        a2: byte = 101;
        a3: byte = 108;
        a4: byte = 108;
        a5: byte = 111;
        a6: byte = 32;
        a7: byte = 119;
        a8: byte = 111;
        a9: byte = 114;
        a10: byte = 108;
        a11: byte = 100;
        a12: byte = 10;
        a13: byte = 0;
    }

    inline _get {
        __org($2)
        [
            - 
            __rel($2, $1) +
            > +
            < __rel($1, $2) 
        ]
        __rel($2, $1)
        [
            - __rel($1, $2)
            + __rel($2, $1)
        ]
        __rel($1, $2)
        [
            -
            __rel($2, $1) +
            >> +
            << __rel($1, $2)
        ]
        __rel($2, $1)
        [
            - __rel($1, $2)
            + __rel($2, $1)
        ]
        >[>>>[-<<<<+>>>>]<<[->+<]<[->+<]>-]
        >>>[-<+<<+>>>]<<<[->>>+<<<]>
        [[-<+>]>[-<+>]<<<<[->>>>+<<<<]>>-]<<
        __rel($1, $0) [-]
        __rel($0, $1) >>>
        [
            - 
            <<< __rel($1, $0) +
            >>> __rel($0, $1)
        ]
        <<< __ret($1)
    }

    inline _puts {
        __org($0) >>>
        [-]
        >
        [.>]
        <
        [<]
        <<< __ret($0)
    }

    inline _inc {
        __org($0)
        +
        __ret($0)
    }

    entry {

    }
'''


# res = arr[i]
program = parse(arr)
program.entry_block.body = [
    # # h
    # CallInlineStatement('_get', [ Identifier('res'), Identifier('arr'), Identifier('i') ]),
    # CallInlineStatement('_inc', [ Identifier('i') ]),
    # CallInlineStatement('_print', [ Identifier('res') ]),
    # # e
    # CallInlineStatement('_get', [ Identifier('res'), Identifier('arr'), Identifier('i') ]),
    # CallInlineStatement('_inc', [ Identifier('i') ]),
    # CallInlineStatement('_print', [ Identifier('res') ]),
    # # l
    # CallInlineStatement('_get', [ Identifier('res'), Identifier('arr'), Identifier('i') ]),
    # CallInlineStatement('_inc', [ Identifier('i') ]),
    # CallInlineStatement('_print', [ Identifier('res') ]),
    # # l
    # CallInlineStatement('_get', [ Identifier('res'), Identifier('arr'), Identifier('i') ]),
    # CallInlineStatement('_inc', [ Identifier('i') ]),
    # CallInlineStatement('_print', [ Identifier('res') ]),
    # # o
    # CallInlineStatement('_get', [ Identifier('res'), Identifier('arr'), Identifier('i') ]),
    # CallInlineStatement('_inc', [ Identifier('i') ]),
    # CallInlineStatement('_print', [ Identifier('res') ])
    CallInlineStatement('_puts', [ Identifier('arr') ]),
]

# print(program.inline_routines)

codegen = CodeGenerator(program)
codegen.emit_program()
compiled = codegen.compile(pretty=False)

print(compiled)