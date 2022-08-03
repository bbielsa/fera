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

class ArrayType(Node):
    # contained = type contained within the array
    # count = the number of items in the array 
    def __init__(self, contained, count, value=[]):
        self.contained = contained
        self.count = count
        self.value = value

class Expression(Node):
    pass

class ConstantExpression(Expression):
    def __init__(self, value):
        self.value = value

class BinaryExpression(Expression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

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

class AssignStatement(Statement):
    def __init__(self, id, value):
        self.identifier = id
        self.value = value

class CommandStatement(Statement):
    def __init__(self, command):
        self.command = command

class CallInlineStatement(Statement):
    def __init__(self, name, parameters):
        self.identifier = name
        self.parameters = parameters

class CallProcedureStatement(Statement):
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

class ConditionalStatement(Statement):
    def __init__(self, expression, then_body=[], else_body=[]):
        self.expression = expression
        self.then_body = then_body
        self.else_body = else_body

class ForStatement(Statement):
    def __init__(self, ident, from_value, to_value, body=[]):
        self.identifier = ident
        self.from_value = from_value
        self.to_value = to_value
        self.body = body

class WhileStatement(Statement):
    def __init__(self, expression, body=[]):
        self.expression = expression
        self.body = body

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

class ProcedureBlock(Block):
    def __init__(self, name, body=[], params=[]):
        super().__init__(body)
        self.identifier = name
        self.parameters = params
        self.type = "procedure"

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
