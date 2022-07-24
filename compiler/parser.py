from scope import Identifier
from command import Command
from scope import Identifier, IndexedIdentifier
from io import StringIO

class Statement:
    def __init__(self):
        pass

class DeclareStatement(Statement):
    def __init__(self, id, const=None):
        self.identifier = Identifier(id)
        self.constant = const

    def __repr__(self):
        return f'{self.identifier.name} = {self.constant}'

class Block:
    def __init__(self, block=[]):
        self.body = block

    def __repr__(self):
        builder = StringIO()

        builder.write(self.type)

        if hasattr(self, 'identifier'):
            builder.write(" ")
            builder.write(self.identifier)

        builder.write(" {")
        builder.write("\n")

        for stmt in self.body:
            builder.write("  ")
            builder.write(stmt.__repr__())
            builder.write("\n")

        builder.write("}")

        return builder.getvalue()

class CommandStatement(Statement):
    def __init__(self, command):
        self.command = command

    def __repr__(self):
        return self.command.value

class InlineBlock(Block):
    def __init__(self, name):
        super().__init__()
        self.identifier = name
        self.type = "inline"

class DataBlock(Block):
    def __init__(self, body=[]):
        super().__init__()
        self.body = body
        self.type = "data"

class EntryBlock(Block):
    def __init__(self, body=[]):
        super().__init__()
        self.body = body
        self.type = "entry"

class CallInlineStatement(Statement):
    def __init__(self, name, parameters):
        self.identifier = name
        self.parameters = parameters

class DirectiveStatement(Statement):
    def __init__(self):
        pass

    def __repr__(self):
        names = map(lambda param: f'${param.index}', self.parameters)
        joined = ",".join(names)

        return f'{self.identifier}({joined})'

class OriginDirectiveStatement(DirectiveStatement):
    def __init__(self, base):
        self.parameters = [base]
        self.identifier = "__org"

class ReturnDirectiveStatement(DirectiveStatement):
    def __init__(self, address):
        self.parameters = [address]
        self.identifier = "__ret"

class RelativeDirectiveStatement(DirectiveStatement):
    def __init__(self, base, offset):
        self.parameters = [base, offset]
        self.identifier = "__rel"

class Program:
    def __init__(self, data_block=None, entry_block=None, inline_routines=[], procedures=[]):
        self.data_block = data_block
        self.entry_block = entry_block
        self.inline_routines = inline_routines
        self.procedures = procedures
