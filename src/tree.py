from tokenize import Name
from scope import Identifier
from command import Command
from scope import Identifier, IndexedIdentifier
from io import StringIO

#
# Expressions
#
class Node:
    def __init__(self):
        pass

class Type(Node):
    def __init__(self, name):
        self.name = name

class Expression(Node):
    pass

class ConstantExpression(Expression):
    def __init__(self, value):
        self.value = value

#
# Statements
#

class Statement(Node):
    def __init__(self):
        pass

class DeclareStatement(Statement):
    def __init__(self, id, type, const=None):
        self.identifier = id
        self.type = type
        self.constant = const

class CommandStatement(Statement):
    def __init__(self, command):
        self.command = command

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
        self.identifier = "__org"

class ReturnDirectiveStatement(DirectiveStatement):
    def __init__(self, address):
        self.parameters = [address]
        self.identifier = "__ret"

class RelativeDirectiveStatement(DirectiveStatement):
    def __init__(self, base, offset):
        self.parameters = [base, offset]
        self.identifier = "__rel"

#
# Blocks
#

class Block:
    def __init__(self, block):
        self.body = block

class InlineBlock(Block):
    def __init__(self, name, body=[]):
        super().__init__(body)
        self.identifier = name
        self.type = "inline"

class DataBlock(Block):
    def __init__(self, body=[]):
        super().__init__(body)
        self.body = body
        self.type = "data"

class EntryBlock(Block):
    def __init__(self, body=[]):
        super().__init__(body)
        self.body = body
        self.type = "entry"

class Program:
    def __init__(self, data_block=None, entry_block=None, inline_routines=[], procedures=[]):
        self.data_block = data_block
        self.entry_block = entry_block
        self.inline_routines = inline_routines
        self.procedures = procedures
