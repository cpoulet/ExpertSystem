#!/usr/bin/env python3

import argparse
import re
import os
import collections
from graph import GraphCreator
from tokenizer import tokengenerator

Token = collections.namedtuple('Token', ['type_', 'value'])

class RuleError(Exception):
    pass

class ChildError(Exception):
    pass

class ThenError(Exception):
    pass

class ParsingError(Exception):
    pass

class InputError(Exception):
    pass

class Color:
    def color(self, string):
        return self.red(string) if string == 'False' else self.green(string) if  string == 'True' else self.yellow(string)
    def red(self, string):
        return '\033[1;31m' + string + '\033[1;0m'
    def green(self, string):
        return '\033[1;32m' + string + '\033[1;0m'
    def yellow(self, string):
        return '\033[1;33m' + string + '\033[1;0m'
    def white(self, string):
        return '\033[1;37m' + string + '\033[1;0m'

class Expertsystem:

    def __init__(self, verbose = False):
        self._verbose       = verbose
        self._leafs         = []
        self._queries       = []
        self._knowledges    = []
        self.d              = {}
        self._gCreator       = GraphCreator()

    def parse_file(self, input_):
        with open(input_, 'r') as f:
            for l in f:
                l = re.sub(r'\s', '', l.split('#')[0])

                if not l:
                    continue

                if l[0] == '=':
                    if re.search(r'[^A-Z]', l[1:]):
                        raise ParsingError('Wrong initial facts')
                    self._leafs = list(l[1:])

                elif l[0] == '?':
                    if re.search(r'[^A-Z]', l[1:]):
                        raise ParsingError('Wrong queries')
                    self._queries = list(l[1:])

                else:
                    s = re.search(r'(^[A-Z+|()!^]+)(<?)=>([A-Z+|()!^]+$)', l)
                    if not s:
                        raise ParsingError('Wrong rules')
                    self._knowledges.append(s.string)
#                    self._knowledges.append({'if':s.group(1), 'then':s.group(3), 'used':False })
#                    if s.group(2):
#                        self._knowledges.append({'if':s.group(3), 'then':s.group(1), 'used':False })
        for rules in self._knowledges:
            self._gCreator.parse(rules, self._gCreator.graph)

    def answer_queries(self):
        for q in self._queries:
            print(q)
#            self.d[q] = self.ask(q)

def main():
    parser = argparse.ArgumentParser(description='Read a Knowledge base then answer the queries.')
    parser.add_argument('input', action='store', help='Input file describing the rules.')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    if not os.path.exists(args.input) or not os.path.isfile(args.input):
        raise InputError('File not found: "' + args.input + '".')
    e = Expertsystem(args.verbose)
    e.parse_file(args.input)
    d = e.answer_queries()
    if d and not args.verbose:
        print('\n'.join('{} : {}'.format(k, v) for k, v in d.items()))
    if args.verbose:
        print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error : ' + str(e))
