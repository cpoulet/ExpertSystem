#!/usr/bin/env python3

import unittest
from expreval import ExprEvaluator

class MyTest(unittest.TestCase):
    """Tests for my ExprEvaluator."""

    def setUp(self):
        self.e = ExprEvaluator()

#    def test_error(self):
#        self.assertRaises(self.e.SequenceError, self.e.parse, 'T +')

    def test_simple(self):
        self.assertEqual(self.e.parse('T'), True)
        self.assertEqual(self.e.parse('F'), False)
        print('Simple tests executed !')

    def test_negate(self):
        self.assertEqual(self.e.parse('!T'), False)
        self.assertEqual(self.e.parse('!F'), True)
        self.assertEqual(self.e.parse('!(!T)'), True)
        self.assertEqual(self.e.parse('!(!F)'), False)
        self.assertEqual(self.e.parse('!!T'), True)
        self.assertEqual(self.e.parse('!!F'), False)
        print('NOT tests executed !')

    def test_and(self):
        self.assertEqual(self.e.parse('T + T'), True)
        self.assertEqual(self.e.parse('!T + T'), False)
        self.assertEqual(self.e.parse('T + !T'), False)
        self.assertEqual(self.e.parse('!T + !T'), False)
        self.assertEqual(self.e.parse('(T + T)'), True)
        self.assertEqual(self.e.parse('(!T + T)'), False)
        self.assertEqual(self.e.parse('(T + !T)'), False)
        self.assertEqual(self.e.parse('(!T + !T)'), False)
        print('AND tests executed !')

    def test_or(self):
        self.assertEqual(self.e.parse('T | T'), True)
        self.assertEqual(self.e.parse('!T | T'), True)
        self.assertEqual(self.e.parse('T | !T'), True)
        self.assertEqual(self.e.parse('!T | !T'), False)
        self.assertEqual(self.e.parse('(T | T)'), True)
        self.assertEqual(self.e.parse('(!T | T)'), True)
        self.assertEqual(self.e.parse('(T | !T)'), True)
        self.assertEqual(self.e.parse('(!T | !T)'), False)
        print('OR tests executed !')

    def test_xor(self):
        self.assertEqual(self.e.parse('T ^ T'), False)
        self.assertEqual(self.e.parse('!T ^ T'), True)
        self.assertEqual(self.e.parse('T ^ !T'), True)
        self.assertEqual(self.e.parse('!T ^ !T'), False)
        self.assertEqual(self.e.parse('(T ^ T)'), False)
        self.assertEqual(self.e.parse('(!T ^ T)'), True)
        self.assertEqual(self.e.parse('(T ^ !T)'), True)
        self.assertEqual(self.e.parse('(!T ^ !T)'), False)
        print('XOR tests executed !')

    def test_complex(self):
        self.assertEqual(self.e.parse('(T | (F | T))'), True)
        self.assertEqual(self.e.parse('!(T | (F | T))'), False)
        self.assertEqual(self.e.parse('(F | F | T)'), True)
        self.assertEqual(self.e.parse('( T + F ^ T)'), True)
        self.assertEqual(self.e.parse('(F | F | T) ^ ( T + F ^ T)'), False)
        self.assertEqual(self.e.parse('(F | F | T) ^ ( T + F ^ T) + (T | (F | T))'), False)
        self.assertEqual(self.e.parse('!((F | F | T) ^ ( T + F ^ T) + (T | (F | T)))'), True)
        print('Complex tests executed !')

    def tearDown(self):
        del self.e

if __name__ == "__main__":
    try:
        unittest.main()
    except Exception as e:
        print('Error : ' + str(e))
