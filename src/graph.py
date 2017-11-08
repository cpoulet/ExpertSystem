#!/usr/bin/env python3

import sys
import re
import collections
from tokenizer import tokengenerator

Token = collections.namedtuple('Token', ['type_', 'value'])

class Graph:
    '''
    example :
    self.nodes =
    {
        'A': <graph.Node at 0x104e71dd8>,
        'B': <graph.Node at 0x104e710b8>,
        'C': <graph.Node at 0x104e71ef0>,
        'D': <graph.Node at 0x104e71b38>,
        'F': <graph.Node at 0x104e71f60>
    }
    '''
    def __init__(self):
        self.nodes = {}

    def checkNode(self, label):
        return label in self.nodes

    def addNode(self, label):
        if not self.checkNode(label):
            self.nodes[label] = Node(label)
        return self.nodes[label]

    def updateNode(self, node):
        print("Node '" + node.label + "' updated")

class Node:
    '''
    value   : 'U' or 'T' or 'F'
    parents : [ OPERATOR or FACT, ... ]
    '''
    def __init__(self, label, *args):
        self.label = label
        self.value = 'U'
        self.parents = []
        self.parents += args
        print("Node '" + label + "' created")

    def addParents(self, *args):
        self.parents += args
        return self

class Fact(Node):
    '''
    label   : A, B, ... ,Z
    '''

    def __init__(self, label):
        super().__init__(label)

class Operator(Node):
    '''
    label   : AND or OR or XOR or NOT

    example:
    label   = 'AND'
    parents = ['FACT', 'OPERATOR']
    value   = 'F'
    '''

    def __init__(self, label):
        super().__init__(label)

class GraphCreator:
    '''
    Implementation of a simple recursive descent parser in the frame
    of my project EvalExpr for "l'Ecole 42".

    Here is the BNF grammar I used :

    <rule>      ::= <expr> ('=>' | '<=>') <expr>
    <expr>      ::= <or> {'^' <expr>}
    <or>        ::= <and> {'|' <or>}
    <and>       ::= <factor> {'+' <and>}
    <not>       ::= '!'<not> | <factor>
    <factor>    ::= '('<expr>')' | FACT
    '''

    def __init__(self):
        self.graph = Graph()
        self.TOKENS_SPEC = [
        ('EQ' , r'\<\=\>'),
        ('IMP' , r'\=\>'),
        ('OR' , r'\|'),
        ('AND' , r'\+'),
        ('XOR' , r'\^'),
        ('NOT' , r'\!'),
        ('LB' , r'\('),
        ('RB' , r'\)'),
        ('FACT' , r'[A-Z]'),
        ('WS' , r'\s'),
        ('ERROR' , r'[^A-Z\s()!^+|]')]

    def parse(self, expr, graph = False):
        if type(graph) == Graph:
            self.graph = graph
        self.token_generator = tokengenerator(expr, self.TOKENS_SPEC)
        self.current_token = None
        self.next_token = None
        self._next()
        self._rule()
        if self.next_token:
            raise SequenceError('Wrong token sequence busted. Processing stopped at ' + self.next_token.value)
        return self.graph

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

    def _refuse(self, token_type):
        if self._accept(token_type):
            raise SequenceError('Wrong token sequence busted. Refused : ' + token_type)

    def _rule(self):
        '''
        <rule>      ::= <expr> ('=>' | '<=>') <expr>
        '''
        self.side = 'LEFT'
        left_value = self._expr()
        if self._accept('IMP'):
            self.side = 'RIGHT'
            return self._expr().addParents(left_value)
        elif self._accept('EQ'):
            print('Don\'t work properly')
            right_value = self._expr() 
            left_value.addParents(right_value)
            return right_value.addParents(left_value)
        else:
            raise SequenceError('Expected => or <=>')

    def _expr(self):
        '''
        <expr> ::= <or> {'^' <expr>}
        '''
        expr_value = self._or()
        while self._accept('XOR'):
            return self.addOperator(expr_value, self._expr(), 'XOR')
        return expr_value
            
    def _or(self):
        '''
        <or> ::= <and> {'|' <or>}
        '''
        or_value = self._and()
        while self._accept('OR'):
            return self.addOperator(or_value, self._or(), 'OR')
        return or_value
        
    def _and(self):
        '''
        <and> ::= <factor> {'+' <and>}
        '''
        and_value = self._not()
        while self._accept('AND'):
            return self.addOperator(and_value, self._and(), 'AND')
        return and_value

    def _not(self):
        '''
        <not> ::= '!'<not> | <factor>
        '''
        if self._accept('NOT'):
            return self.addNot(self._not())
        return self._factor()

    def _factor(self):
        '''
        <factor> ::= '('<expr>')' | <fact>
        '''
        if self._accept('FACT'):
            return self.graph.addNode(self.current_token.value)
        elif self._accept('LB'):
            expr_value = self._expr()
            self._expect('RB')
            return expr_value
        else:
            raise SequenceError('Expected a FACT or a Left Brace')

    def addOperator(self, left_n, right_n, label):
        if left_n.label != label and right_n.label != label:
            if self.side == 'LEFT':
                return Operator(label, left_n, right_n)
            else:
                o = Operator(label)
                left_n.addParents(o)
                right_n.addParents(o)
                return o
        elif left_n.label == label:
            if self.side == 'LEFT':
                left_n.addParents(right_n)
                return left_n
            else:
                right_n.addParents(left_n)
                return left_n
        else:
            if self.side == 'LEFT':
                right_n.addParents(left_n)
                return right_n
            else:
                left_n.addParents(right_n)
                return right_n

    def addNot(self, node):
        if self.side == 'LEFT':
            return Operator('NOT', node)
        else:
            o = Operator('NOT')
            node.addParents(o)
            return o

class SequenceError(Exception):
    pass

class TokenError(Exception):
    pass

class ArgumentError(Exception):
    pass

def main(argv):
    if len(argv) != 2:
        raise ArgumentError('Only one argument is needed.')
    e = GraphCreator()
    graph = e.parse(argv[1])
    graph = e.parse(argv[1], graph)

if __name__ == "__main__":
    try:
	    main(sys.argv)
    except Exception as e:
        print('Error : ' + str(e))
        '''
        A => B + C
        D => C
        '''
