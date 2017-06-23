#!/usr/bin/env python3

import sys
import re
import collections

Token = collections.namedtuple('Token', ['type_', 'value'])

def tokenize(expr, tokens_spec):
    '''Token Generator'''
    token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens_spec))
    for item in re.finditer(token_regex, expr):
        if not item.lastgroup == 'WS':
            yield Token(item.lastgroup, item.group())

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
        ('WS' , r'\s')]

    def parse(self, expr):
        self.token_generator = tokenize(expr, self.TOKENS_SPEC)
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
            raise Exception('Wrong token sequence busted. Expected : ' + token_type)

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
        and_value = self._factor()
        while self._accept('AND'):
            return and_value and self._and()
        return and_value

    def _factor(self):
        '''
        <factor> ::= '('<expr>')' | <fact>
        '''
        if self._accept('FACT'):
            return True if self.current_token.value == 'A' else False
        elif self._accept('LB'):
            expr_value = self._expr()
            self._expect('RB')
            return expr_value
        else:
            raise Exception('Expected a FACT or a Left Brace')

def main(argv):
    if len(argv) != 2:
        raise Exception('Only one argument is needed.')
    e = ExprEvaluator()
    print(e.parse(argv[1]))

if __name__ == "__main__":
    try:
	    main(sys.argv)
    except Exception as e:
        print('Error : ' + str(e))
