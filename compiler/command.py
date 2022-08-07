from enum import Enum

class Command(Enum):
    SEEK_LEFT = "<"
    SEEK_RIGHT = ">"
    INC = "+"
    DEC = "-"
    OUT = "."
    IN = ","
    JUMP = "["
    LOOP = "]"

    def parse(char=None):
        for cmd in Command:
            if cmd.value == char:
                return cmd

class Comment:
    def __init__(self, comment):
        self.comment = comment
