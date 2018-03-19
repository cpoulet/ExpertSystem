import re
import collections

from node import Node, Fact, Operator
from exceptions import ArgumentError, SequenceError
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

    def addFact(self, label):
        if not self.checkNode(label):
            self.nodes[label] = Fact(label)
        return self.nodes[label]

    def addOperator(self, label, leftNode=None, rightNode=None, side=True):
        if side:
            o = Operator(label)
            o.setParents(leftNode, rightNode)
        else:
            o = Operator(label)
            o.addChildren([leftNode, rightNode])
        return o

    def updateNode(self, node):
        # Do stuff here ?
        print("Node '" + node.label + "' updated")


class GraphCreator:
    '''
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
        ('IFF' , r'\<\=\>'),
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

    def parse(self, expr, graph=False):
        if type(graph) is Graph: 
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
            return self.graph.addOperator('XOR', leftNode=expr_value, rightNode=self._expr())
        return expr_value
            
    def _or(self):
        '''
        <or> ::= <and> {'|' <or>}
        '''
        or_value = self._and()
        while self._accept('OR'):
            return self.graph.addOperator('OR', leftNode=or_value, rightNode=self._or())
        return or_value
        
    def _and(self):
        '''
        <and> ::= <factor> {'+' <and>}
        '''
        and_value = self._not()
        while self._accept('AND'):
            return self.graph.addOperator('AND', leftNode=and_value, rightNode=self._and())
        return and_value

    def _not(self):
        '''
        <not> ::= '!'<not> | <factor>
        '''
        if self._accept('NOT'):
            return self.graph.addOperator('NOT', leftNode=self._not())
        return self._factor()

    def _factor(self):
        '''
        <factor> ::= '('<expr>')' | <fact>
        '''
        if self._accept('FACT'):
            return self.graph.addFact(self.current_token.value)
        elif self._accept('LB'):
            expr_value = self._expr()
            self._expect('RB')
            return expr_value
        else:
            raise SequenceError('Expected a FACT or a Left Brace')
