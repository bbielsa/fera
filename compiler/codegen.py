from scope import Identifier, IndexedIdentifier, Scope
from parser import Program, DeclareStatement, CallInlineStatement, OriginDirectiveStatement, ReturnDirectiveStatement, CommandStatement
from parser import DataBlock, EntryBlock, InlineBlock
from command import Command, Comment
import pprint

class Allocator:
    @classmethod
    def sizeof(self, declaractions):
        return len(declaractions.body)

    @classmethod
    def reserve(self, size, base=0):
        return range(base, base + size)

class CodeGenerator:
    def __init__(self, program):
        self.data_regions = []

        self.program = program
        self.global_scope = Scope(None, 0)
        self.scope = self.global_scope
        self.scopes = [self.scope]

        self.compiled = []
    
    def scope_base_heap(self, scope):
        if scope.id == 0:
            return 0
        
        id = scope.id
        region = self.data_regions[id]

        return region[0]

    def allocate(self, ident):

        # if self.global_scope == self.scope:
        scope_idents = self.scope.identifiers
        scope_size = len(scope_idents)
        scope_base = self.scope_base_heap(self.scope)

        if ident.name == "z":
            print("scope_base", scope_base)
            print("scope_size", scope_size)
        ident.heap_pointer = scope_base + scope_size
        #     ident.heap_pointer = scope_size
        # else:
        #     raise ValueError()

        self.scope.add(ident)

    def emit_program(self):
        data_block = self.program.data_block
        entry_block = self.program.entry_block

        self.emit_comment("Data Segment")

        self.scope = self.global_scope
        self.emit_block(data_block)

        self.emit_comment("Text Segment")
        self.push_scope()
        self.emit_block(entry_block)
        self.pop_scope()
    
    def push_scope(self, new_scope=None):
        if new_scope == None:
            new_scope_id = len(self.scopes)
            new_scope = Scope(self.scope, new_scope_id)

        self.scope.children.add(new_scope)
        self.scope = new_scope
    
    def pop_scope(self):
        if self.scope.parent == None:
            raise ValueError()

        self.scope = self.scope.parent

    def emit_data_segment(self, data_block):
        self.emit_block(data_block)

    def emit_block(self, block):
        # maybe this belongs in push_scope()?
        size = Allocator.sizeof(block)
        region = Allocator.reserve(size)

        self.data_regions.append(region)

        return self.emit_body(block.body)

    def emit_body(self, body):
        for stmt in body:
            self.emit_statement(stmt)

    def emit_seek(self, count):
        self.emit_repeat(count, Command.SEEK_RIGHT)
    
    def emit_initialize(self, count):
        self.emit_repeat(count, Command.INC)

    def emit_return(self, count):
        self.emit_repeat(count, Command.SEEK_LEFT)

    def emit_repeat(self, count, command):
        for i in range(count):
            self.emit_command(command)

    def emit_command(self, command):
        self.compiled.append(command)

    def emit_comment(self, comment):
        cmd = Comment(comment)
        self.emit_command(cmd)

    def emit_declare(self, stmt):
        ident = stmt.identifier
        
        self.allocate(ident)

        if stmt.constant == None:
            return
        else:
            self.emit_seek(ident.heap_pointer)
            self.emit_initialize(stmt.constant)
            self.emit_return(ident.heap_pointer)

    def emit_statement(self, stmt):
        if type(stmt) == DeclareStatement:
            self.emit_declare(stmt)
        elif type(stmt) == CallInlineStatement:
            self.emit_call_inline(stmt)
        else:
            print(type(stmt))
            raise ValueError()

    def emit_origin_directive(self, stmt, params):
        origin = self.bind_parameter(stmt.parameters[0], params)

        self.emit_seek(origin.heap_pointer)

    def emit_return_directive(self, stmt, params):
        ret = self.bind_parameter(stmt.parameters[0], params)

        self.emit_return(ret.heap_pointer)

    def _program_get_inline_routine(self, name):
        blocks = filter(
            lambda r: r.identifier == name,
            self.program.inline_routines
        )

        return next(blocks)

    def emit_call_inline(self, stmt):
        name = stmt.identifier
        params = stmt.parameters

        routine = self._program_get_inline_routine(name)

        self.emit_inline_routine(routine, params)

    def bind_parameter(self, index_identifier, params):
        index = index_identifier.index
        param = params[index]
        name = param.name
        print(self.scope[name].heap_pointer)
        print("parameter", index, "is", name)

        return self.scope[name]

    def emit_inline_routine(self, routine, parameters):
        for stmt in routine.body:
            if type(stmt) == OriginDirectiveStatement:
                self.emit_origin_directive(stmt, parameters)
            elif type(stmt) == ReturnDirectiveStatement:
                self.emit_return_directive(stmt, parameters)
            elif type(stmt) == CommandStatement:
                self.emit_command(stmt.command)

    def compile(self, pretty=True):
        result = ""
        column_size = 24
        cursor = 0

        for command in self.compiled:
            if type(command) == Command:
                cursor += 1
                result += command.value

                if cursor == 24:
                    result += "\n"
                    cursor = 0
            elif type(command) == Comment:
                result += "\n"
                result += command.comment
                result += "\n"

        return result


clear = InlineBlock("_clr")
clear.body = [
    OriginDirectiveStatement(IndexedIdentifier(0)),
    CommandStatement(Command.JUMP),
    CommandStatement(Command.DEC),
    CommandStatement(Command.LOOP),
    ReturnDirectiveStatement(IndexedIdentifier(0))
]

dadd = InlineBlock("_dadd")
dadd.body = [
    OriginDirectiveStatement(IndexedIdentifier(0)),
    
    CommandStatement(Command.JUMP),

    ReturnDirectiveStatement(IndexedIdentifier(0)),
    OriginDirectiveStatement(IndexedIdentifier(1)),
    CommandStatement(Command.INC),

    ReturnDirectiveStatement(IndexedIdentifier(1)),
    OriginDirectiveStatement(IndexedIdentifier(0)),
    CommandStatement(Command.DEC),

    CommandStatement(Command.LOOP),
    
    ReturnDirectiveStatement(IndexedIdentifier(0))
]

p = Program(
    data_block=DataBlock(body=[
        DeclareStatement('x'),
        DeclareStatement('a', 4),
        DeclareStatement('b', 6),
        DeclareStatement('c', 255)
    ]),
    entry_block=EntryBlock(body=[
        CallInlineStatement('_clr', [ Identifier('c') ]),
        CallInlineStatement('_dadd', [ Identifier('a'), Identifier('c') ]),
        CallInlineStatement('_dadd', [ Identifier('b'), Identifier('c') ]),
    ]),
    inline_routines=[
        clear,
        dadd
    ],
    procedures=[

    ]
)
c = CodeGenerator(p)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(p)

c.emit_program()
print(c.compile())
