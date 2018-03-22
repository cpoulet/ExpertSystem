#!/usr/bin/env python3

import argparse
import re
import os
import collections

from node import *
from color import Color
from graph import GraphCreator
from tokenizer import tokengenerator
from exceptions import GraphError, ParsingError

Token = collections.namedtuple('Token', ['type_', 'value'])

class Expertsystem:

    def __init__(self, verbose = False):
        self._verbose       = verbose
        self._leafs         = None
        self._queries       = None
        self._knowledges    = []
        self._gCreator      = GraphCreator(verbose)

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
                    self._knowledges.append(s[1] + '=>' + s[3])
                    if s[2] == '<':
                        self._knowledges.append(s[3] + '=>' + s[1])
        self._checkParsing()
        self._createGraph()

    def _checkParsing(self):
        if self._leafs == None or self._queries == None or self._knowledges == []:
            raise ParsingError('Missing input data')

    def _createGraph(self):
        for rules in self._knowledges:
            self._gCreator.parse(rules, self._gCreator.graph)
        for l in self._leafs:
            if l in self._gCreator.graph.nodes:
                self._gCreator.graph.nodes[l].setValue('True')

    def answerQueries(self):
        C = Color()
        for q in self._queries:
            if q in self._gCreator.graph.nodes:
                print(q + ' is ' + C.color(self.askNode(self._gCreator.graph.nodes[q])))
            else:
                print(q + ' is ' + C.color('False'))

    def askNode(self, node, seen=set()):
        seen.add(node.label)
        if self._verbose:
            print('Asking', node)
        if not node.parents:
            return node.value
        if type(node) is Operator:
            return node.setValue(self._evalOperator(node))
        for p in node.parents:
            if p.label not in seen:
                node.setValue(self.askNode(p, seen))
        return node.value

    def _evalOperator(self, operator):
        
        if operator.label == 'NOT':
            left = self.askNode(operator.parents[0])
            if self._verbose:
                print('Evaluating NOT with', left)
            if left == 'True':
                return 'False'
            elif left == 'False':
                return 'True'
            else:
                return 'Undefined'

        if operator.children:
            value = self.askNode(operator.parents[0])
            return self._solve(operator, value)

        if operator.label == 'AND':
            left = self.askNode(operator.parents[0])
            right = self.askNode(operator.parents[1])
            if self._verbose:
                print('Evaluating AND with', operator.parents[0].label, '=', left, 'and', operator.parents[1].label, '=', right)
            if left == 'False' or right == 'False':
                return 'False'
            if left == 'Undefined' or right == 'Undefined':
                return 'Undefined'
            else:
                return 'True'

        if operator.label == 'OR':
            left = self.askNode(operator.parents[0])
            right = self.askNode(operator.parents[1])
            if self._verbose:
                print('Evaluating OR with', operator.parents[0].label, '=', left, 'and', operator.parents[1].label, '=', right)
            if left == 'True' or right == 'True':
                return 'True'
            if left == 'Undefined' or right == 'Undefined':
                return 'Undefined'
            else:
                return 'False'

        if operator.label == 'XOR':
            left = self.askNode(operator.parents[0])
            right = self.askNode(operator.parents[1])
            if self._verbose:
                print('Evaluating XOR with', operator.parents[0].label, '=', left, 'and', operator.parents[1].label, '=', right)
            if left == 'Undefined' or right == 'Undefined':
                return 'Undefined'
            if left == right:
                return 'False'
            else:
                return 'True'
        
        raise GraphError('This graph is not possible')

    def _solve(self, node, value):

        if type(node) is Fact:
            return node.setValue(value)

        if (node.label == 'AND' and value == 'True') or (node.label == 'OR' and value == 'False'):
            for child in node.children:
                self._solve(child, value)
            return value
        
        else:
            return 'Undefined'

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
