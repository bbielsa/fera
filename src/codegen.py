from tree import ForStatement, WhileStatement
from tree import Type, ArrayType
from scope import Identifier, IndexedIdentifier, Scope
from tree import CallProcedureStatement
from tree import ConstantExpression
from tree import AssignStatement
from tree import RelativeDirectiveStatement
from tree import Program, DeclareStatement, CallInlineStatement, OriginDirectiveStatement, ReturnDirectiveStatement, CommandStatement
from tree import DataBlock, EntryBlock, InlineBlock
from command import Command, Comment
import pprint

class Cell:
    def __init__(self, heap_pointer=None):
        self.heap_pointer = heap_pointer

class StaticAllocator:
    array_header_size = 4

    def __init__(self):
        self.size = 0
        self.members = []

    @classmethod
    def sizeof(self, t):
        if type(t) == Type:
            return 1
        elif type(t) == ArrayType:
            contained_type = t.contained
            contained_size = StaticAllocator.sizeof(contained_type)

            return t.count * contained_size + StaticAllocator.array_header_size

    def reserve(self, ident, type):
        size = StaticAllocator.sizeof(type)
        ident.heap_pointer = self.size
        self.members.append((ident, type))
        self.size += size

    def alloc(self, type):
        cell = Cell()
        self.reserve(cell, type)

        return cell

    def free(self, cell):
        pass

class CodeGenerator:
    def __init__(self, program):
        self.data_regions = []

        self.program = program
        self.global_scope = Scope(None, 0)
        self.scope = self.global_scope
        self.scopes = [self.scope]

        self.allocator = StaticAllocator()

        self.compiled = []
    
    def scope_base_heap(self, scope):
        if scope.id == 0:
            return 0
        
        id = scope.id
        region = self.data_regions[id]

        return region[0]

    def allocate(self, ident, type):
        self.allocator.reserve(ident, type)
        self.scope.add(ident)

    def emit_program(self):
        data_block = self.program.data_block
        entry_block = self.program.entry_block

        self.emit_comment("Data Segment")

        self.scope = self.global_scope
        self.emit_block(data_block)

        self.emit_comment("Text Segment")
        # print(entry_block.body)
        self.emit_block(entry_block)
    
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
        # size = Allocator.sizeof(block)
        # region = Allocator.reserve(size)

        # self.data_regions.append(region)

        return self.emit_body(block.body)

    def emit_body(self, body):
        for stmt in body:
            self.emit_statement(stmt)

    def emit_seek(self, count):
        self.emit_repeat(count, Command.SEEK_RIGHT)
    
    def emit_initialize(self, count):
        self.emit_repeat(count.value, Command.INC)

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

    def emit_initialize_string(self, ident, type, constant):
        byte_array = map(
            lambda c: ConstantExpression(ord(c)),
            constant.value
        )
        byte_array = list(byte_array)

        self.emit_initialize_array(ident, type, byte_array)

    def emit_initialize_array(self, ident, type, constant):
        count = type.count
        items = len(constant)

        size = min(count, items)

        self.emit_seek(ident.heap_pointer)
        self.emit_seek(StaticAllocator.array_header_size)
        
        for i in range(size):
            self.emit_initialize(constant[i])
            self.emit_seek(1)

        self.emit_return(
            ident.heap_pointer
            + size
            + StaticAllocator.array_header_size
        )

    def emit_declare(self, stmt):
        ident = stmt.identifier   

        self.allocate(stmt.identifier, stmt.type)

        if stmt.constant == None:
            return

        if type(stmt.type) == ArrayType and type(stmt.constant) == list:
            self.emit_initialize_array(ident, stmt.type, stmt.constant)
        elif type(stmt.type) == ArrayType and type(stmt.constant) == ConstantExpression:
            self.emit_initialize_string(ident, stmt.type, stmt.constant)
        else:
            self.emit_seek(ident.heap_pointer)
            self.emit_initialize(stmt.constant)
            self.emit_return(ident.heap_pointer)

    def emit_for(self, stmt):
        ident = stmt.identifier
        from_value = stmt.from_value
        to_value = stmt.to_value
        
        self.allocate(ident, Type("byte"))

        # initialize x
        self.emit_seek(ident.heap_pointer)
        self.emit_clear_cell(ident.heap_pointer)
        self.emit_initialize(from_value)
        
        # evaluate x
        self.emit_repeat(to_value.value + 1, Command.DEC)

        # loop
        self.emit_command(Command.JUMP)

        # restore x
        self.emit_repeat(to_value.value + 1, Command.INC)
        self.emit_return(ident.heap_pointer)

        #execute the body
        self.emit_body(stmt.body)

        # evaluate the loop condition and loop or break
        self.emit_seek(ident.heap_pointer)
        self.emit_repeat(to_value.value + 1, Command.DEC)
        self.emit_command(Command.INC)
        self.emit_command(Command.LOOP)
        self.emit_return(ident.heap_pointer)

    def emit_statement(self, stmt):
        if type(stmt) == DeclareStatement:
            self.emit_declare(stmt)
        elif type(stmt) == CallInlineStatement:
            self.emit_call_inline(stmt)
        elif type(stmt) == AssignStatement:
            self.emit_assign_statement(stmt)
        elif type(stmt) == CallProcedureStatement:
            self.emit_call_procedure(stmt)
        elif type(stmt) == ForStatement:
            self.emit_for(stmt)
        elif stmt == None:
            pass
        else:
            print("Error statement type not implemented")
            print(type(stmt))
            raise NotImplementedError()

    def emit_call_procedure(self, stmt):
        raise NotImplementedError()

    def emit_expression(self, expr):
        cell_type = Type("byte")
        cell = self.allocator.alloc(cell_type)

        if type(expr) == ConstantExpression:
            self.emit_seek(cell.heap_pointer)
            self.emit_clear_cell(None)
            self.emit_repeat(expr.value, Command.INC)
            self.emit_return(cell.heap_pointer)

            return cell
        elif type(expr) == Identifier:
            ident = self.scope[expr.name]
            return ident

        lhs = self.emit_expression(expr.left)
        rhs = self.emit_expression(expr.right)

        # Add operand 1
        self.emit_seek(lhs.heap_pointer)
        self.emit_command(Command.JUMP)
        self.emit_return(lhs.heap_pointer)
        self.emit_seek(cell.heap_pointer)
        self.emit_command(Command.INC)
        self.emit_return(cell.heap_pointer)
        self.emit_seek(lhs.heap_pointer)
        self.emit_command(Command.DEC)
        self.emit_command(Command.LOOP)
        self.emit_return(lhs.heap_pointer)

        # Add operand 2
        self.emit_seek(rhs.heap_pointer)
        self.emit_command(Command.JUMP)
        self.emit_return(rhs.heap_pointer)
        self.emit_seek(cell.heap_pointer)
        self.emit_command(Command.INC)
        self.emit_return(cell.heap_pointer)
        self.emit_seek(rhs.heap_pointer)
        self.emit_command(Command.DEC)
        self.emit_command(Command.LOOP)
        self.emit_return(rhs.heap_pointer)

        self.allocator.free(lhs)
        self.allocator.free(rhs)

        return cell

    def emit_assign_statement(self, stmt):
        dest_cell = self.scope[stmt.identifier.name]
        source_cell = self.emit_expression(stmt.value)

        self.emit_seek(source_cell.heap_pointer)
        self.emit_command(Command.JUMP)
        self.emit_return(source_cell.heap_pointer)
        self.emit_seek(dest_cell.heap_pointer)
        self.emit_command(Command.INC)
        self.emit_return(dest_cell.heap_pointer)
        self.emit_seek(source_cell.heap_pointer)
        self.emit_command(Command.DEC)
        self.emit_command(Command.LOOP)
        self.emit_return(source_cell.heap_pointer)

    def emit_clear_cell(self, cell):
        self.emit_command(Command.JUMP)
        self.emit_command(Command.DEC)
        self.emit_command(Command.LOOP)

    def emit_origin_directive(self, stmt, params):
        origin = self.bind_parameter(stmt.parameters[0], params)

        self.emit_seek(origin.heap_pointer)

    def emit_return_directive(self, stmt, params):
        ret = self.bind_parameter(stmt.parameters[0], params)
        self.emit_return(ret.heap_pointer)

    def emit_relative_directive(self, stmt, params):
        origin = self.bind_parameter(stmt.parameters[0], params)
        dest = self.bind_parameter(stmt.parameters[1], params)

        relative = dest.heap_pointer - origin.heap_pointer

        if relative > 0:
            self.emit_seek(relative)
        elif relative < 0:
            relative = abs(relative)
            self.emit_return(relative)

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

        return self.scope[name]

    def emit_inline_routine(self, routine, parameters):
        for stmt in routine.body:
            if type(stmt) == OriginDirectiveStatement:
                self.emit_origin_directive(stmt, parameters)
            elif type(stmt) == ReturnDirectiveStatement:
                self.emit_return_directive(stmt, parameters)
            elif type(stmt) == RelativeDirectiveStatement:
                self.emit_relative_directive(stmt, parameters)
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

                if pretty and cursor == 24:
                    result += "\n"
                    cursor = 0
            elif pretty and type(command) == Comment:
                result += "\n"
                result += command.comment
                result += "\n"

        return result
