import sys
from io import StringIO
from .ply.lex import lex
from .ply.yacc import yacc


tokens = (
    'LSQBRACKET', 'RSQBRACKET', 'PLUS', 
    'MINUS', 'LPTBRACKET', 'RPTBRACKET',
    'POINT', 'COMMA'
)

t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_LPTBRACKET = r'<'
t_RPTBRACKET = r'>'
t_POINT = r'\.'
t_COMMA = r','

def t_error(t):
    t.lexer.skip(1)

def p_error(p):
    pass

def p_program(p):
    '''
    program : cmd_list
    '''
    p[0] = p[1]

def p_cmd_list_1(p):
    '''
    cmd_list : cmd
    '''
    p[0] = [p[1]]

def p_cmd_list_2(p):
    '''
    cmd_list : cmd_list cmd
    '''
    p[0] = p[1] + [p[2]]

def p_cmd_loop(p):
    '''
    cmd : LSQBRACKET cmd_list RSQBRACKET
    '''
    p[0] = [p[1]] + p[2] + [p[3]]

def p_cmd(p):
    '''
    cmd : PLUS
        | MINUS
        | LPTBRACKET
        | RPTBRACKET
        | POINT
        | COMMA
    '''
    p[0] = p[1]

def pprint(program, out, depth=0, tab_size=2, max_column=40):
    indent = ' ' * tab_size * depth
    column = 0

    out.write(indent)

    for cmd in program:    
        if type(cmd) == str:
            out.write(cmd)
            column += 1

            if column > max_column:
                out.write("\n")
                out.write(indent)
                column = 0
        elif type(cmd) == list:
            open = cmd.pop(0)
            close = cmd.pop()
            out.write("\n")
            out.write(indent)
            out.write(open)
            out.write("\n")
            pprint(cmd, out, depth=depth+1, tab_size=tab_size)
            out.write(indent)
            out.write(close + "\n")
            out.write(indent)

    out.write("\n")

def format(code, tab_size=2):
    lexer = lex()
    parser = yacc()
    ast = parser.parse(code)
    
    with StringIO() as out:
        pprint(ast, out, tab_size=tab_size)
        return out.getvalue()
