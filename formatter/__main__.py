import argparse
from .format import format

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Format brainfuck code')
    parser.add_argument('path', type=str, help='.bf file path')
    parser.add_argument('--indent', type=int, default=2, help='size of indents in spaces')

    args = parser.parse_args()
    
    with open(args.path) as f:
        code = f.read()
        formatted = format(code, tab_size=args.indent)

        print(formatted)
