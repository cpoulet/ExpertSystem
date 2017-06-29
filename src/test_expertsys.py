#!/usr/bin/env python3

import unittest
from expertsys import *

class MyTest(unittest.TestCase):
    """Tests for my ExprSystem."""

    def setUp(self):
        self.e = Expertsystem()

    def test_simple_1(self):
        self.e.parse_file('../test/test_simple/simple_1.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':True})

    def test_simple_2(self):
        self.e.parse_file('../test/test_simple/simple_2.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':False})

    def test_simple_3(self):
        self.e.parse_file('../test/test_simple/simple_3.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':False})

    def test_simple_4(self):
        self.e.parse_file('../test/test_simple/simple_4.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':True})

    def test_simple_5(self):
        self.e.parse_file('../test/test_simple/simple_5.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':False})

    def test_simple_6(self):
        self.e.parse_file('../test/test_simple/simple_6.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':True})

    def test_simple_7(self):
        self.e.parse_file('../test/test_simple/simple_7.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':False})

    def test_simple_8(self):
        self.e.parse_file('../test/test_simple/simple_8.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':False})

    def test_simple_9(self):
        self.e.parse_file('../test/test_simple/simple_9.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':False})

    def test_simple_10(self):
        self.e.parse_file('../test/test_simple/simple_10.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':True})

    def test_simple_11(self):
        self.e.parse_file('../test/test_simple/simple_11.txt')
        self.assertDictEqual(self.e.answer_queries(), {'A':True, 'B':True, 'C':True, 'E':'undefined', 'F':False ,'K':False})

    def _test_error(self):
        self.e.parse_file('../test/error/error_parsing_1.txt')
        self.e.answer_queries()
        print('Error tests executed !')

    def tearDown(self):
        del self.e

if __name__ == "__main__":
    try:
        unittest.main()
    except Exception as e:
        print('Error : ' + str(e))
