#!/usr/bin/env python3

import argparse
import re
import os
import collections
from expreval import ExprEvaluator
from tokenizer import tokengenerator

Token = collections.namedtuple('Token', ['type_', 'value'])

class Answer:

    def __init__(self):
        self.facts = [False] * 26
        self.modified = [False] * 26

    def show(self):
        print(*[chr(c + 65) for c in range(26)])
        print(*['T' if x == True else 'F' if x == False else 'U' for x in self.facts])

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

class Node:

    def __init__(self, name, root = False, children = []):
        self.name = name
        self.root = root
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
        print(*ret)

    def p_prefix(self):
        print (self.name)
        for child in self.children:
            child.p_prefix()

    def p_suffix(self):
        for child in self.children:
            child.p_suffix()
        print (self.name)

    def e_suffix(self, answer = False, verbose = False):
        for child in self.children:
            child.e_suffix(answer, verbose)
        self._evaluate(answer, verbose)

    def _evaluate(self, answer, verbose):
        if not self.root:
            e = ExprEvaluator(answer)
            rslt = e.parse(self.name['if'])
            if verbose:
                print('\t' + self.name['if'] + ' is ' + str(rslt) + ' implies ', end = '')
                print(self.name['then'] + ' is ' + str(rslt))
            self._involve(rslt, self.name['then'], answer, verbose)

    def _involve(self, rslt, rule, answer, verbose):
        regex = re.compile('(?P<FACT>^[A-Z]$)|(?P<NOT>^\![A-Z]$)|(?P<AND>^[A-Z]\+[A-Z]$)|(?P<OR>^[A-Z]\|[A-Z]$)')
        match = re.match(regex, rule)
        if not match:
            raise ThenError('The "Then" part is a bit too complex')
        if match.lastgroup == 'FACT':
            self._modify(match.group()[0], answer, rslt)
        elif match.lastgroup == 'NOT':
            self._modify(match.group()[1], answer, not rslt)
        elif match.lastgroup == 'AND':
            if rslt: 
                self._modify(match.group()[0], answer, rslt)
                self._modify(match.group()[2], answer, rslt)
            else: 
                self._modify(match.group()[0], answer, 'undefined')
                self._modify(match.group()[2], answer, 'undefined')
        elif match.lastgroup == 'OR':
            if not rslt: 
                self._modify(match.group()[0], answer, rslt)
                self._modify(match.group()[2], answer, rslt)
            else: 
                self._modify(match.group()[0], answer, 'undefined')
                self._modify(match.group()[2], answer, 'undefined')

    def _modify(self, fact, answer, value):
        k = ord(fact) - 65
        if answer.facts[k] != value:
            if answer.modified[k] and answer.facts[k] != 'undefined' and value != 'undefined':
                raise RuleError('There is an insolving incoherance between rules')
            elif value != 'undefined' or not answer.modified[k]:
                answer.facts[k] = value
        answer.modified[k] = True

class Expertsystem:

    def __init__(self, verbose = False):
        self._verbose       = verbose
        self._leafs         = []
        self._queries       = []
        self._knowledges    = []
        self.d              = {}
        self.a              = Answer()

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

        for l in self._leafs:
            self.a.facts[ord(l) - 65] = True
            self.a.modified[ord(l) - 65] = True

    def answer_queries(self):
        for q in self._queries:
            self.d[q] = self.ask(q)
        return self.d

    def ask(self, fact):
        if self._verbose:
            print('\nAsking value of ' + fact + ':\n')
        if fact in self._leafs:
            if self._verbose:
                print('\t' + fact + ' is a True initial fact')
            return True
        root = Node(fact, True)
        for rule in self._knowledges:
            if fact in rule['then'] and not rule['used']:
                child = root.add_child(Node(rule))
                self._firing_rule(child, rule)
        if self._verbose and len(self._leafs):
            print('\t', end ='')
            print(*self._leafs, sep=',', end='')
            print(' is True' if len(self._leafs) == 1 else ' are True')
        root.e_suffix(self.a, self._verbose)
        if self._verbose:
            print('\t' + root.name + ' is ' + str(self.a.facts[ord(root.name) - 65]))
        self._reinit()
        return self.a.facts[ord(root.name) - 65]

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
