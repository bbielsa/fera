import argparse
from . import Fera

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