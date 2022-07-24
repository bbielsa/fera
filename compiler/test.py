from parser import Program, DeclareStatement, CallInlineStatement, OriginDirectiveStatement, ReturnDirectiveStatement, CommandStatement
from parser import DataBlock, EntryBlock, InlineBlock, Command, RelativeDirectiveStatement
from scope import Identifier, IndexedIdentifier
import json

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
    
    RelativeDirectiveStatement(IndexedIdentifier(0), IndexedIdentifier(1)),
    ReturnDirectiveStatement(IndexedIdentifier(1)),
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

print(p.inline_routines[1])