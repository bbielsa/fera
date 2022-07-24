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

class Comment:
    def __init__(self, comment):
        self.comment = comment
