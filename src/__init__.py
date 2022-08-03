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
        i: byte = 9;

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
        _get(res, arr, i);
        _puts(arr);
    }
'''

easy = '''
    data {
        a: byte = 104;
    }

    inline _clr {
        __org($0)
        [-]
        __ret($0)
    }

    inline _putc {
        __org($0)
        .
        __ret($0)
    }

    proc hello(x: byte) {
        _putc(x);
        x = 105;
        _putc(x);
        x = 60;
        _putc(x);
        x = 51;
        _putc(x);
        x = 10;
        _putc(x);
        _clr(x);
    }

    entry {
        if a {
            a = 200;
        }
        else {
            a = 50;
        }
        _clr(a);
    }
'''

loops = '''
    data {
        x: byte = 0;
        y: byte = 10;
    }

    entry {
        for x = 0...y {
            x = 10;
        }

        while x {
            x = 0;
        }
    }
'''

'''

1 * 2 + 1 * 4

       +
     /   \
    /     \
   /       \
1 * 2     1 * 4

1. 1 * 4 = r0
2. 1 * 2 = r1
3. r0 + r1 = r0


1 * (3 + 2) * 4 + 6


1. 3 + 2 = r0
2. r0 
'''

math = '''
    data {
        a: byte = 1;
        b: byte;
    }

    entry {
        b = 2 / 3;
    }
'''

decl_array = '''
    data {
        z: byte = 24;
        y: byte[10];
        w: byte[200] = { 1, 2, 3, 4 };
        a: byte[13] = { 72,69,76,76,79,32,87,79,82,76,68,33 };
        x: byte = 25;
    }

    inline _puts {
        __org($0)
        >>>>
        [.>]
        <
        [<]
        <<<
        __ret($0)
    }

    entry {
        _puts(a);
    }
'''

program = parse(decl_array)
# print(program.data_block.body[1].constant[2].value)
codegen = CodeGenerator(program)
codegen.emit_program()
compiled = codegen.compile(pretty=False)

print(compiled)