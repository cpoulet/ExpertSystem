#!/usr/bin/env python3

import argparse
import re
import os
import collections
from expreval import ExprEvaluator
from tokenizer import tokengenerator

Token = collections.namedtuple('Token', ['type_', 'value'])

class Node:

    def __init__(self, name, children = []):
        self.name = name
        self.children = []
        for child in children:
            self.add_child(Node(child))

    def add_child(self, child):
        if not isinstance(child, Node):
            raise ChildError('Child problem. Openning the Fridge...')
        self.children.append(child)
        return child

    def p_breadth(self):
        ret = []
        queue = []
        queue.append(self)
        while queue:
            for child in queue[0].children:
                queue.append(child)
            ret.append(queue[0].name)
            del queue[0]
        return ret

    def p_prefix(self):
        print (self.name)
        for child in self.children:
            child.p_prefix()

    def p_suffix(self):
        for child in self.children:
            child.p_suffix()
        print (self.name)

class Expertsystem:

    def __init__(self, verbose):
        self._verbose       = verbose
        self._leafs         = []
        self._queries       = []
        self._knowledges    = []

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
                    self._knowledges.append({'if':s.group(1), 'then':s.group(3), 'used':False })
                    if s.group(2):
                        self._knowledges.append({'if':s.group(3), 'then':s.group(1), 'used':False })

        if self._verbose:
            print('Leafs = ' + str(self._leafs))
            print('Queries = ' + str(self._queries))
            print(*self._knowledges, sep='\n')

    def answer_queries(self):
        for q in self._queries:
            self.ask(q)

    def ask(self, fact):
        if fact in self._leafs:
            print(fact + ' is True.')
            return
        root = Node(fact)
        for rule in self._knowledges:
            if fact in rule['then'] and not rule['used']:
                child = root.add_child(Node(rule))
                self._firing_rule(child, rule)
        print(*root.p_breadth(), sep='\n')
        self._reinit()

    def _firing_rule(self, node, rule):
        rule['used'] = True
        for fact in re.finditer(r'[A-Z]', rule['if']):
            if fact.group() not in self._leafs:
                for r in self._knowledges:
                    if fact.group() in r['then'] and not r['used']:
                        child = node.add_child(Node(r))
                        self._firing_rule(child, r)
    
    def _reinit(self):
        for rule in self._knowledges:
            rule['used'] = False

def main():
    parser = argparse.ArgumentParser(description='Read a Knowledge base then answer the queries.')
    parser.add_argument('input_', action='store', help='Input file describing the rules.')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    if not os.path.exists(args.input_) or not os.path.isfile(args.input_):
        raise InputError('File not found: "' + args.input_ + '".')
    e = Expertsystem(args.verbose)
    e.parse_file(args.input_)
    e.answer_queries()

if __name__ == "__main__":
    main()
#    try:
#        main()
#    except Exception as e:
#        print('Error : ' + str(e))
