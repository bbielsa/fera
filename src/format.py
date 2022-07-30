import sys
from ply.lex import lex
from ply.yacc import yacc


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

def pprint(program, depth=0, tab='  '):
    indent = tab * depth

    print(indent, sep="", end="")

    for cmd in program:    
        if type(cmd) == str:
            print(cmd, sep="", end="")
        elif type(cmd) == list:
            open = cmd.pop(0)
            close = cmd.pop()
            print()
            print(indent, sep="", end="")
            print(open, sep="", end="")
            print()
            pprint(cmd, depth=depth+1)
            print(indent, sep="", end="")
            print(close)
            print(indent, sep="", end="")
    print()

def format():
    if len(sys.argv) != 2:
        print("Usage: python3 format.py <filename>")
        return

    program_path = sys.argv[1]

    with open(program_path) as f:
        source = f.read()
        parser = yacc()
        ast = parser.parse(source)
        
        pprint(ast)

if __name__ == '__main__':
    lexer = lex()
    parser = yacc()

    format()
