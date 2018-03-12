#!/usr/bin/env python3

import sys
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

    if type(tokens_spec) is not list:
        raise Exception('Error: The token_spec argument should be a list')
    token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in tokens_spec))
    for item in re.finditer(token_regex, expr):
        if item.lastgroup == 'ERROR':
            raise TokenError('Very wrong token.')
        if not item.lastgroup == 'WS':
            yield Token(item.lastgroup, item.group())

def main(argv):
    if len(argv) not in [2,3]:
        raise Exception('usage: ' + argv[0] + ' expression [token_spec]')
    expr = argv[1]
    if len(argv) == 3:
        token_spec = argv[2]
    else:
        token_spec = [
            ('OR' , r'\|'),
            ('AND' , r'\+'),
            ('XOR' , r'\^'),
            ('NOT' , r'\!'),
            ('LB' , r'\('),
            ('RB' , r'\)'),
            ('FACT' , r'[A-Z]'),
            ('WS' , r'\s'),
            ('ERROR' , r'[^A-Z\s()!^+|]'),
        ]
    tg = tokengenerator(expr, token_spec)
    for token in tg:
        print(token)

if __name__ == "__main__":
    main(sys.argv)
#    try:
#        main(sys.argv)
#    except Exception as e:
#        print(str(e))
