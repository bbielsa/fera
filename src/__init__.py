from parser import parse
from scope import Identifier
from tree import CallInlineStatement
from codegen import CodeGenerator

code = '''
    data {
        x: byte = 10;
        r: byte;
    }

    entry {
        x = x + 90;
        r = x;
    }
'''

program = parse(code)
# print(program.data_block.body[1].constant[2].value)
codegen = CodeGenerator(program)
codegen.emit_program()
compiled = codegen.compile(pretty=False)

print(compiled)