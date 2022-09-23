from . import Fera
import argparse

code = '''
    data {
        x: byte = 104;
        r: byte;
        z: byte[100];
        nl: byte = 10;
    }

    inline _putc {
        __org($0)
        .
        __ret($0)
    }

    entry {
        r = x;
        _putc(x);
        r = r + 1;
        _putc(r);
        _putc(nl);
    }
'''

parser = argparse.ArgumentParser(description="Command line frontend for the fera language compiler")

parser.add_argument("-p",
    dest="pretty",
    action="store_true",
    help="Pretty print the output")

parser.add_argument("filename",
    help="Fera input file")

args = parser.parse_args()

with open(args.filename) as f:
    compiled = Fera.compile(f, args.pretty)
    print(compiled)