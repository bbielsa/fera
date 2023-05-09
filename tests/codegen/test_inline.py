import unittest
from brainfuck import BrainfuckInterpreter
from compiler import Fera


class TestInline(unittest.TestCase):
    def _run(self, code):
        compiled = Fera.compiles(code)
        bf = BrainfuckInterpreter(compiled)

        while bf.available():
            bf.step()

        return bf

    def test_inline_arg(self):
        code = '''
        data {
            x: byte = 10;
        }

        inline _inc {
            __org($0)
            +
            __ret($0)
        }

        entry {
            _inc(x);
        }
        '''
        bf = self._run(code)

        self.assertEqual(11, bf.cells[0])
