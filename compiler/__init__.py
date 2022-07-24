from ply.lex import lex
from ply.yacc import yacc
from util import flatten_productions

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 
    'KWDATA', 'KWPROC', 'KWENTRY', 'LBRACKET', 'RBRACKET', 
    'LPAREN', 'RPAREN',
    'TYPE', 'IDENT', 'IIDENT', 'DIDENT', 'COLON', 'SEMICOLON', 
    'ASSIGN', 'LITERAL', 'KWINLINE',
    'LSQBRACKET', 'RSQBRACKET', 'PLUS', 'MINUS', 'LPTBRACKET',
    'RPTBRACKET', 'POINT', 'COMMA'
)

# Ignored characters
t_ignore = ' \t'

RESERVED = {
    'data': 'KWDATA',
    'entry': 'KWENTRY',
    'proc': 'KWPROC',
    'inline': 'KWINLINE',
    'byte': 'TYPE'
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
t_LPTBRACKET = r'<'
t_RPTBRACKET = r'>'
t_POINT = r'\.'
t_COMMA = r','

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
    r'_{2}[a-zA-Z]+'
    t.type = RESERVED.get(t.value, 'DIDENT')
    return t

def t_IIDENT(t):
    r'\$[0-9]+'
    t.type = RESERVED.get(t.value, 'IIDENT')
    return t

# def t_COMMAND(t):
#     r'[\[\]\+\-\<\>\.\,]'
#     t.type = RESERVED.get(t.value, 'COMMAND')
#     return t

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
    program : data_block 
            | data_block code_block_region entry_block
            | empty
    '''
    _, *blocks = p
    p[0] = ('program', *blocks)

def p_empty(p):
    '''
    empty : 
    '''

def p_code_block_region(p):
    '''
    code_block_region : proc_block code_block_region
                      | inline_block code_block_region
                      | empty
    '''
    _, *stmts = p
    code_blocks = flatten_productions(stmts)
    p[0] = code_blocks

def p_proc_block(p):
    '''
    proc_block : KWPROC LBRACKET RBRACKET
    '''
    p[0] = ('proc', [])

def p_inline_block(p):
    '''
    inline_block : KWINLINE DIDENT LBRACKET inline_region RBRACKET
    '''
    stmts = flatten_productions(p[4])
    p[0] = ('inline', p[2], stmts)

def p_entry_block(p):
    '''
    entry_block : KWENTRY LBRACKET RBRACKET
    '''
    p[0] = ('entry', [])

def p_data_block(p):
    '''
    data_block : KWDATA LBRACKET init_region RBRACKET
    '''
    count = len(p)

    if count == 4:
        p[0] = ('data', [])
    else:
        init_stmts = flatten_productions(p[3])
        p[0] = ('data', init_stmts)

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

def p_inline_stmt(p):
    '''
    inline_stmt : command_statement
                | directive_stmt
    '''
    p[0] = p[1]

def p_directive_args_list(p):
    # 
    '''
    directive_args_list : IIDENT
                        | IIDENT COMMA directive_args_list
                        | empty
    '''
    p[0] = p[1]

def p_directive_args(p):
    '''
    directive_args : LPAREN directive_args_list RPAREN
    '''
    p[0] = p[2]

def p_directive_stmt(p):
    '''
    directive_stmt : DIDENT directive_args
    '''
    p[0] = ('directive', p[1], p[2])

def p_init_region(p):
    '''
    init_region : init_stmt init_region
                | empty
    '''
    _, *stmts = p
    p[0] = stmts

def p_init_stmt(p):
    '''
    init_stmt : IDENT COLON TYPE SEMICOLON
              | IDENT COLON TYPE ASSIGN LITERAL SEMICOLON
    '''
    is_init = len(p) == 7
    
    if is_init:
        p[0] = ('init_stmt', p[1], p[3], p[5])
    else:
        p[0] = ('init_stmt', p[1], p[3])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

if __name__ == "__main__":
    # Build the parser
    parser = yacc(debug=True)

    program = '''
        data {
            a: byte = 255;
        }

        inline __clr {
            __org($0)
            __rel($0, $1)
            [-]
            __ret($0)
        }

        entry {

        }
    '''

    # Parse an expression
    ast = parser.parse(program)
    print(ast)
