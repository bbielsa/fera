from ast import Index
from ply.lex import lex
from ply.yacc import yacc
from scope import Identifier
from tree import WhileStatement
from tree import ForStatement
from tree import ConditionalStatement
from tree import ProcedureBlock
from tree import CallInlineStatement
from tree import CallProcedureStatement
from tree import AssignStatement
from tree import ReturnDirectiveStatement, BinaryExpression
from tree import OriginDirectiveStatement, RelativeDirectiveStatement
from tree import Program
from tree import InlineBlock
from tree import DataBlock
from tree import EntryBlock
from tree import ConstantExpression
from tree import DeclareStatement, Type, ArrayType
from tree import CommandStatement
from scope import IndexedIdentifier
from command import Command
from util import flatten_productions, flatten_productions_sep

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 
    'KWDATA', 'KWPROC', 'KWENTRY', 'LBRACKET', 'RBRACKET', 
    'LPAREN', 'RPAREN', 'IF', 'ELSE', 'FOR', 'WHILE', 'ASTERISK', 'FSLASH',
    'TYPE', 'IDENT', 'IIDENT', 'DIDENT', 'COLON', 'SEMICOLON', 
    'ASSIGN', 'LITERAL', 'KWINLINE',
    'LSQBRACKET', 'RSQBRACKET', 'PLUS', 'MINUS', 'LPTBRACKET',
    'RPTBRACKET', 'POINT', 'COMMA', 'ELLIPSIS'
)

# Ignored characters
t_ignore = ' \t'

RESERVED = {
    'data': 'KWDATA',
    'entry': 'KWENTRY',
    'proc': 'KWPROC',
    'inline': 'KWINLINE',
    'byte': 'TYPE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE'
}

# Token matching rules are written as regexs
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_COLON = r':'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_ASTERISK = r'\*'
t_FSLASH = r'/'
t_LPTBRACKET = r'<'
t_RPTBRACKET = r'>'
t_POINT = r'\.'
t_COMMA = r','
t_ELLIPSIS = r'\.\.\.'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'LITERAL'
    return t

def t_IDENT(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = RESERVED.get(t.value, 'IDENT')
    return t

def t_DIDENT(t):
    r'_{,2}[a-zA-Z]+'
    t.type = RESERVED.get(t.value, 'DIDENT')
    return t

def t_IIDENT(t):
    r'\$[0-9]+'
    t.type = RESERVED.get(t.value, 'IIDENT')
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Parser

def p_program(p):
    '''
    program : data_block code_block_region entry_block
            | empty
    '''
    _, *blocks = p

    if blocks[0] == None:
        p[0] = Program()
        return

    data_block = blocks.pop(0)
    entry_block = blocks.pop()
    code_blocks = blocks[0]

    p[0] = Program(data_block=data_block, entry_block=entry_block, inline_routines=code_blocks)

def p_empty(p):
    '''
    empty : 
    '''

def p_code_block_region_1(p):
    '''
    code_block_region : proc_block
                      | inline_block
                      | empty
    '''
    p[0] = [p[1]]

def p_code_block_region_2(p):
    '''
    code_block_region : code_block_region proc_block
                      | code_block_region inline_block
    '''
    p[0] = p[1] + [p[2]]

def p_proc_block(p):
    '''
    proc_block : KWPROC IDENT proc_params LBRACKET stmt_list RBRACKET
    '''
    p[0] = ProcedureBlock(p[2], body=p[5], params=p[3])

def p_inline_block(p):
    '''
    inline_block : KWINLINE DIDENT LBRACKET inline_region RBRACKET
    '''
    name = p[2]
    stmts = flatten_productions(p[4])
    # p[0] = ('inline', p[2], stmts)
    p[0] = InlineBlock(name, body=stmts)
    
def p_param_decl(p):
    '''
    param_decl : IDENT COLON type
    '''
    p[0] = DeclareStatement(p[1], p[3])

def p_param_decl_list_1(p):
    '''
    param_decl_list : param_decl
                    | empty
    '''
    p[0] = [p[1]]

def p_param_decl_list_2(p):
    '''
    param_decl_list : param_decl_list COMMA param_decl
    '''
    p[0] = p[1] + [p[3]]

def p_proc_params(p):
    '''
    proc_params : LPAREN param_decl_list RPAREN
    '''
    p[0] = p[2]

def p_entry_block(p):
    '''
    entry_block : KWENTRY LBRACKET stmt_list RBRACKET
    '''
    p[0] = EntryBlock(p[3])

def p_stmt_list_1(p):
    '''
    stmt_list : stmt
              | empty
    '''
    p[0] = [p[1]]

def p_stmt_list_2(p):
    '''
    stmt_list : stmt_list stmt
    '''
    p[0] = p[1] + [p[2]]

def p_stmt(p):
    '''
    stmt : assign_stmt SEMICOLON
         | call_proc_stmt SEMICOLON
         | call_inline_stmt SEMICOLON
         | conditional_stmt
         | for_stmt
         | while_stmt
    '''
    p[0] = p[1]

def p_while_stmt(p):
    '''
    while_stmt : WHILE rval LBRACKET stmt_list RBRACKET
    '''
    p[0] = WhileStatement(p[2], body=p[4])

def p_for_stmt(p):
    '''
    for_stmt : FOR identifier ASSIGN rval ELLIPSIS rval LBRACKET stmt_list RBRACKET
    '''
    p[0] = ForStatement(p[2], p[4], p[6], body=p[8])

def p_conditional_stmt(p):
    '''
    conditional_stmt : IF rval LBRACKET stmt_list RBRACKET
                     | IF rval LBRACKET stmt_list RBRACKET ELSE LBRACKET stmt_list RBRACKET
    '''
    p[0] = ConditionalStatement(p[2], then_body=p[4], else_body=p[8])

def p_call_arg(p):
    '''
    call_arg : rval
    '''
    p[0] = p[1]

def p_call_args_list_1(p):
    '''
    call_args_list : call_arg
                   | empty
    '''
    p[0] = [p[1]]

def p_call_args_list_2(p):
    '''
    call_args_list : call_args_list COMMA call_arg
    '''
    p[0] = p[1] + [p[3]]

def p_call_args(p):
    '''
    call_args : LPAREN call_args_list RPAREN
    '''
    p[0] = p[2]

def p_call_proc_stmt(p):
    '''
    call_proc_stmt : IDENT call_args
    '''
    p[0] = CallProcedureStatement(p[1], p[2])

def p_call_inline_stmt(p):
    '''
    call_inline_stmt : DIDENT call_args
    '''
    p[0] = CallInlineStatement(p[1], p[2])

def p_assign_stmt(p):
    '''
    assign_stmt : identifier ASSIGN expr
    '''
    p[0] = AssignStatement(p[1], p[3])

def p_binary_expr(p):
    '''
    expr : expr PLUS expr
         | expr MINUS expr
    '''
    p[0] = BinaryExpression(p[2], p[1], p[3])

def p_expr_term(p):
    '''
    expr : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : term ASTERISK term
         | term FSLASH term
    '''
    p[0] = BinaryExpression(p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_paren(p):
    '''
    factor : LPAREN expr RPAREN
    '''
    p[0] = p[2]

def p_factor(p):
    '''
    factor : identifier
           | constant_expression
    '''
    p[0] = p[1]

def p_rval(p):
    '''
    rval : expr
    '''
    p[0] = p[1]

def p_data_block(p):
    '''
    data_block : KWDATA LBRACKET init_region RBRACKET
    '''
    count = len(p)

    if count == 4:
        p[0] = DataBlock()
    else:
        init_stmts = flatten_productions(p[3])
        p[0] = DataBlock(init_stmts)

def p_inline_region(p):
    '''
    inline_region : inline_stmt inline_region
                  | empty
    '''
    _, *stmts = p
    p[0] = stmts

def p_command_stmt(p):
    '''
    command_statement : PLUS
                      | MINUS
                      | RSQBRACKET
                      | LSQBRACKET
                      | RPTBRACKET
                      | LPTBRACKET
                      | POINT
                      | COMMA
    '''
    command = Command.parse(p[1])
    stmt = CommandStatement(command)
    p[0] = stmt

def p_inline_stmt(p):
    '''
    inline_stmt : command_statement
                | directive_stmt
    '''
    p[0] = p[1]

def p_directive_args_list_1(p):
    '''
    directive_args_list : IIDENT
    '''
    name = p[1]
    index = int(name[1:])
    p[0] = [ IndexedIdentifier(index) ]

def p_directive_args_list_2(p):
    '''
    directive_args_list : directive_args_list COMMA IIDENT 
    '''
    name = p[3]
    index = int(name[1:])
    p[0] = p[1] + [ IndexedIdentifier(index) ]

def p_directive_args(p):
    '''
    directive_args : LPAREN directive_args_list RPAREN
    '''
    p[0] = p[2]

def p_directive_stmt(p):
    '''
    directive_stmt : DIDENT directive_args
    '''
    name = p[1]
    args = p[2]

    if name == '__org':
        p[0] = OriginDirectiveStatement(args[0])
    elif name == '__ret':
        p[0] = ReturnDirectiveStatement(args[0])
    elif name == '__rel':
        p[0] = RelativeDirectiveStatement(args[0], args[1])

    # p[0] = ('directive', p[1], p[2])

def p_init_region(p):
    '''
    init_region : init_stmt init_region
                | empty
    '''
    _, *stmts = p
    p[0] = stmts

def p_init_stmt(p):
    '''
    init_stmt : identifier COLON type ASSIGN constant_expression SEMICOLON
              | identifier COLON type SEMICOLON
    '''
    is_init = len(p) == 7
    init_id = p[1]
    init_type = p[3]

    if is_init:
        value = p[5]
        p[0] = DeclareStatement(init_id, init_type, value)
    else:
        p[0] = DeclareStatement(init_id, init_type)

def p_identifier(p):
    '''
    identifier : IDENT
    '''

    name = p[1]
    identifier = Identifier(name)
    p[0] = identifier

def p_type(p):
    '''
    type : TYPE
    '''
    name = p[1]
    parsed_type = Type(name)
    p[0] = parsed_type

def p_type_array(p):
    '''
    type : type LSQBRACKET LITERAL RSQBRACKET
    '''
    contained = p[1]
    count = int(p[3])
    p[0] = ArrayType(contained, count)

def p_const_array_expr(p):
    '''
    const_array_expr : LBRACKET const_expr_list RBRACKET
    '''
    p[0] = p[2]

def p_type_array_init(p):
    '''
    type : type LSQBRACKET LITERAL RSQBRACKET const_array_expr
    '''
    contained = p[1]
    count = int(p[3])
    expr = p[5]
    p[0] = ArrayType(contained, count, value=expr)

def p_const_expr_list_1(p):
    '''
    const_expr_list : constant_expression
    '''
    p[0] = [p[1]]

def p_const_expr_list_2(p):
    '''
    const_expr_list : const_expr_list COMMA constant_expression
    '''
    p[0] = p[1] + [p[3]]

def p_constant_expression(p):
    '''
    constant_expression : LITERAL
    '''
    value = int(p[1])
    constant = ConstantExpression(value)
    p[0] = constant

def p_error(p):
    print(f'Syntax error at {p.value!r} {p.lineno}')

def parse(program):
    parser = yacc()
    ast = parser.parse(program)

    return ast
