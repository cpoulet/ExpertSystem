from exceptions import ContradictionError

class Node:
    '''
    Attributes:
    children    : [ Node, ... ]
    label       : 'A', 'B', ... , 'Z'
    parents     : (Node, Node) || (Node, None) || (None, None)
    value       : 'U' or 'T' or 'F' (default: 'F')

    Methods:
    addChildren : (children=[ Node, ... ]) => Node
    setParents  : (parent1=Node, parent2=Node) => Node
    '''
    def __init__(self, label):
        self.children = []
        self.label = label
        self.parents = (None, None)
        self.value = 'F'
        self._set = False
        print("Node '" + label + "' created")

    def addChildren(self, children=[]):
        self.children += children
        return self

    def setParents(self, parent1=None, parent2=None):
        self.parents = (parent1, parent2)
        return self

    def setValue(self, value):
        if self._set and self.value != value:
            raise ContradictionError('Two rules are in contradiction.')
        self._set = True
        self.value = value
        return self.value

class Fact(Node):
    '''
    label   : 'A', 'B', ... , 'Z'

    example:
    children = [ Operator('AND') ]
    label   = 'A'
    parents = ( Operator('NOT'), None )
    value   = 'T'
    '''
    def __init__(self, label):
        super().__init__(label)

    def __repr__(self):
        if self.parents[1]:
            return "Fact: label({}) parents({},{}) value({})".format(self.label, self.parents[0].label, self.parents[1].label, self.value)
        if self.parents[0]:
            return "Fact: label({}) parents({}) value({})".format(self.label, self.parents[0].label, self.value)
        else:
            return "Fact: label({}) value({})".format(self.label, self.value)

class Operator(Node):
    '''
    label   : 'NOT' || 'AND' || 'OR' || 'XOR' || 'IMP' || 'IFF'

    example:
    children = [ Operator('IMP') ]
    label   = 'AND'
    parents = ( Fact('A'), Fact('B') )
    value   = 'F'
    '''
    def __init__(self, label):
        super().__init__(label)

    def __repr__(self):
        if self.parents[1]:
            return "Operator: label({}) parents({},{}) value({})".format(self.label, self.parents[0].label, self.parents[1].label, self.value)
        else:
            return "Operator: label({}) parents({}) value({})".format(self.label, self.parents[0].label, self.value)
