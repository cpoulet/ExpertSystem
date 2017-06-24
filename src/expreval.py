#!/usr/bin/env python3

import sys
import re
import collections
from tokenizer import tokengenerator

Token = collections.namedtuple('Token', ['type_', 'value'])

class ExprEvaluator:
    '''
    Implementation of a simple recursive descent parser in the frame
    of my project EvalExpr for "l'Ecole 42".

    Here is the BNF grammar I used :

    <expr>      ::= <or> {'^' <expr>}
    <or>        ::= <and> {'|' <or>}
    <and>       ::= <factor> {'+' <and>}
    <not>       ::= '!'<not> | <factor>
    <factor>    ::= '('<expr>')' | FACT
    '''

    def __init__(self):
        self.TOKENS_SPEC = [
        ('OR' , r'\|'),
        ('AND' , r'\+'),
        ('XOR' , r'\^'),
        ('NOT' , r'\!'),
        ('LB' , r'\('),
        ('RB' , r'\)'),
        ('FACT' , r'[A-Z]'),
        ('WS' , r'\s'),
        ('ERROR' , r'[^A-Z\s()!^+|]')]

    def parse(self, expr):
        self.token_generator = tokengenerator(expr, self.TOKENS_SPEC)
        self.current_token = None
        self.next_token = None
        self._next()
        return self._expr()

    def _next(self):
        self.current_token, self.next_token = self.next_token, next(self.token_generator, None)

    def _accept(self, token_type):
        if self.next_token and self.next_token.type_ == token_type:
            self._next()
            return True
        else:
            return False

    def _expect(self, token_type):
        if not self._accept(token_type):
            raise SequenceError('Wrong token sequence busted. Expected : ' + token_type)

    def _expr(self):
        '''
        <expr> ::= <or> {'^' <expr>}
        '''
        expr_value = self._or()
        while self._accept('XOR'):
            return expr_value ^ self._expr()
        return expr_value
            
    def _or(self):
        '''
        <or> ::= <and> {'|' <or>}
        '''
        or_value = self._and()
        while self._accept('OR'):
            return or_value | self._or()
        return or_value
        
    def _and(self):
        '''
        <and> ::= <factor> {'+' <and>}
        '''
        and_value = self._not()
        while self._accept('AND'):
            return and_value & self._and()
        return and_value

    def _not(self):
        '''
        <not> ::= '!'<not> | <factor>
        '''
        if self._accept('NOT'):
            return not self._not()
        return self._factor()

    def _factor(self):
        '''
        <factor> ::= '('<expr>')' | <fact>
        '''
        if self._accept('FACT'):
            return True if self.current_token.value == 'T' else False
        elif self._accept('LB'):
            expr_value = self._expr()
            self._expect('RB')
            return expr_value
        else:
            raise SequenceError('Expected a FACT or a Left Brace')

class SequenceError(ValueError):
    pass

class TokenError(ValueError):
    pass

class ArgumentError(ValueError):
    pass

def main(argv):
    if len(argv) != 2:
        raise ArgumentError('Only one argument is needed.')
    e = ExprEvaluator()
    print(e.parse(argv[1]))

if __name__ == "__main__":
    try:
	    main(sys.argv)
    except Exception as e:
        print('Error : ' + str(e))
