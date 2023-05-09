import unittest
from brainfuck import BrainfuckInterpreter
from compiler import Fera


class TestAssign(unittest.TestCase):
    def _run(self, code):
        compiled = Fera.compiles(code)
        bf = BrainfuckInterpreter(compiled)

        while bf.available():
            bf.step()

        return bf

    def test_declare(self):
        code = '''
        data {
            x: byte = 10;
        }
        entry { }
        '''
        bf = self._run(code)

        self.assertEqual(10, bf.cells[0])

    def test_assign_copy(self):
        code = '''
        data {
            x: byte = 20;
            y: byte;
        }

        entry {
            y = x;
        }
        '''

        bf = self._run(code)

        self.assertEqual(20, bf.cells[0])
        self.assertEqual(20, bf.cells[1])

    def test_assign(self):
        code = '''
        data {
            x: byte;
        }

        entry {
            x = 15;
        }
        '''

        bf = self._run(code)

        self.assertEqual(15, bf.cells[0])
