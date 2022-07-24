from scope import Identifier
from command import Command
from scope import Identifier, IndexedIdentifier

class Statement:
    def __init__(self):
        pass

class DeclareStatement(Statement):
    def __init__(self, id, const=None):
        self.identifier = Identifier(id)
        self.constant = const

class Block:
    def __init__(self):
        self.body = []

class InlineBlock(Block):
    def __init__(self, name):
        super().__init__()
        self.identifier = name

class CommandStatement:
    def __init__(self, command):
        self.command = command

class DataBlock(Block):
    def __init__(self, body=[]):
        super().__init__()
        self.body = body

class EntryBlock(Block):
    def __init__(self, body=[]):
        super().__init__()
        self.body = body

class CallInlineStatement(Statement):
    def __init__(self, name, parameters):
        self.identifier = name
        self.parameters = parameters

class DirectiveStatement(Statement):
    def __init__(self):
        pass

class OriginDirectiveStatement(DirectiveStatement):
    def __init__(self, base):
        self.parameters = [base]

class ReturnDirectiveStatement(DirectiveStatement):
    def __init__(self, address):
        self.parameters = [address]

class Program:
    def __init__(self, data_block=None, entry_block=None, inline_routines=[], procedures=[]):
        self.data_block = data_block
        self.entry_block = entry_block
        self.inline_routines = inline_routines
        self.procedures = procedures
