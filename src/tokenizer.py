#!/usr/bin/env python3

import re
import collections

Token = collections.namedtuple('Token', ['type_', 'value'])

def tokengenerator(expr, tokens_spec):
    '''
    Token Generator

    Example of a token specification list:

        tokens_spec = [
        ('OR' , r'\|'),
        ('AND' , r'\+'),
        ('XOR' , r'\^'),
        ('NOT' , r'\!'),
        ('LB' , r'\('),
        ('RB' , r'\)'),
        ('FACT' , r'[A-Z]'),
        ('WS' , r'\s'),
        ('ERROR' , r'[^A-Z\s()!^+|]')]

    Description of Token named tuple:

        Token = collections.namedtuple('Token', ['type_', 'value'])
    '''

    token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens_spec))
    for item in re.finditer(token_regex, expr):
        if item.lastgroup == 'ERROR':
            raise TokenError('Very wrong token.')
        if not item.lastgroup == 'WS':
            yield Token(item.lastgroup, item.group())
