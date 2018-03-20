#!/usr/bin/env python3

import argparse
import re
import os
import collections

from node import *
from graph import GraphCreator
from tokenizer import tokengenerator
from exceptions import GraphError, ParsingError

Token = collections.namedtuple('Token', ['type_', 'value'])

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
        self._gCreator      = GraphCreator()

    def parseFile(self, input_):
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
        for rules in self._knowledges:
            self._gCreator.parse(rules, self._gCreator.graph)
        self._initFact()

    def _initFact(self):
        for l in self._leafs:
            self._gCreator.graph.nodes[l].setValue('T')

    def answerQueries(self):
        for q in self._queries:
            print(q, 'is', self.askNode(self._gCreator.graph.nodes[q]))

    def askNode(self, node):
        if self._verbose:
            print('Asking', node)
        if node.parents == (None, None):
            return node.value
        if type(node) is Operator:
            return node.setValue(self._evalOperator(node))
        for p in node.parents:
            if p:
                return self.askNode(p)
        raise GraphError('This graph is not possible')

    def _evalOperator(self, operator):
        #A faire plus propre
        if operator.label == 'NOT':
            left = self.askNode(operator.parents[0])
            if self._verbose:
                print('Evaluating NOT with', left)
            if left == 'T':
                return 'F'
            elif left == 'F':
                return 'T'
            else:
                return 'U'

        if operator.label == 'AND':
            left = self.askNode(operator.parents[0])
            right = self.askNode(operator.parents[1])
            if self._verbose:
                print('Evaluating AND with', operator.parents[0].label, '=', left, 'and', operator.parents[1].label, '=', right)
            if left == 'F' or right == 'F':
                return 'F'
            if left == 'U' or right == 'U':
                return 'U'
            else:
                return 'T'

        if operator.label == 'OR':
            left = self.askNode(operator.parents[0])
            right = self.askNode(operator.parents[1])
            if self._verbose:
                print('Evaluating OR with', operator.parents[0].label, '=', left, 'and', operator.parents[1].label, '=', right)
            if left == 'T' or right == 'T':
                return 'T'
            if left == 'U' or right == 'U':
                return 'U'
            else:
                return 'F'

        if operator.label == 'XOR':
            left = self.askNode(operator.parents[0])
            right = self.askNode(operator.parents[1])
            if self._verbose:
                print('Evaluating XOR with', operator.parents[0].label, '=', left, 'and', operator.parents[1].label, '=', right)
            if left == 'U' or right == 'U':
                return 'U'
            if left == right:
                return 'F'
            else:
                return 'T'
        
        raise GraphError('This graph is not possible')

def main():
    parser = argparse.ArgumentParser(description='Read a Knowledge base then answer the queries.')
    parser.add_argument('input', action='store', help='Input file describing the rules.')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    if not os.path.exists(args.input) or not os.path.isfile(args.input):
        raise InputError('File not found: "' + args.input + '".')
    e = Expertsystem(args.verbose)
    e.parseFile(args.input)
    d = e.answerQueries()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error : ' + str(e))
