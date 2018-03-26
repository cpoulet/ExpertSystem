#!/usr/bin/env python3

import unittest
from expertsys import *
from exceptions import *

class MyTest(unittest.TestCase):
    """Tests for my ExprSystem."""

    def setUp(self):
        self.e = Expertsystem(verbose=False, quiet=True)

    def test_error_6(self):
        self.assertRaises(SequenceError, self.e.parseFile, '../test/test_error/error_parsing_6.txt')

    def test_error_7(self):
        self.assertRaises(ParsingError, self.e.parseFile, '../test/test_error/error_parsing_7.txt')

    def test_error_8(self):
        self.assertRaises(ParsingError, self.e.parseFile, '../test/test_error/error_parsing_8.txt')

    def test_error_9(self):
        self.assertRaises(ParsingError, self.e.parseFile, '../test/test_error/error_parsing_9.txt')

    def test_error_10(self):
        self.assertRaises(ParsingError, self.e.parseFile, '../test/test_error/error_parsing_10.txt')

    def test_error_rule_1(self):
        self.e.parseFile('../test/test_error/error_rule_1.txt')
        self.assertRaises(ContradictionError, self.e.answerQueries)

    def test_error_rule_2(self):
        self.e.parseFile('../test/test_error/error_rule_2.txt')
        self.assertRaises(ContradictionError, self.e.answerQueries)

#    def test_error_then_1(self):
#        self.e.parseFile('../test/test_error/error_then_1.txt')
#        self.assertRaises(ThenError, self.e.answerQueries)

    def test_simple_1(self):
        self.e.parseFile('../test/test_simple/simple_1.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'True'})

    def test_simple_2(self):
        self.e.parseFile('../test/test_simple/simple_2.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'False'})

    def test_simple_3(self):
        self.e.parseFile('../test/test_simple/simple_3.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'False'})

    def test_simple_4(self):
        self.e.parseFile('../test/test_simple/simple_4.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'True'})

    def test_simple_5(self):
        self.e.parseFile('../test/test_simple/simple_5.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'False'})

    def test_simple_6(self):
        self.e.parseFile('../test/test_simple/simple_6.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'True'})

    def test_simple_7(self):
        self.e.parseFile('../test/test_simple/simple_7.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'False'})

    def test_simple_8(self):
        self.e.parseFile('../test/test_simple/simple_8.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'False'})

    def test_simple_9(self):
        self.e.parseFile('../test/test_simple/simple_9.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'False'})

    def test_simple_10(self):
        self.e.parseFile('../test/test_simple/simple_10.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'True'})

    def test_simple_11(self):
        self.e.parseFile('../test/test_simple/simple_11.txt')
        self.assertDictEqual(self.e.answerQueries(), {'E':'Undefined'})

    def test_complex_1(self):
        self.e.parseFile('../test/test_complex/complex_1.txt')
        self.assertDictEqual(self.e.answerQueries(), {'A':'True', 'B':'True', 'C':'True', 'E':'Undefined', 'F':'False' ,'K':'False'})

    def test_complex_2(self):
        self.e.parseFile('../test/test_complex/complex_2.txt')
        self.assertDictEqual(self.e.answerQueries(), {'G':'True', 'V':'True', 'X':'True'})

    def test_complex_3(self):
        self.e.parseFile('../test/test_complex/complex_3.txt')
        self.assertDictEqual(self.e.answerQueries(), {'G':'True', 'V':'True', 'X':'True', 'H':'False'})

    def _test_error(self):
        self.e.parseFile('../test/error/error_parsing_1.txt')
        self.e.answerQueries()
        print('Error tests executed !')

    def tearDown(self):
        del self.e

if __name__ == "__main__":
    try:
        unittest.main()
    except Exception as e:
        print('Error : ' + str(e))
