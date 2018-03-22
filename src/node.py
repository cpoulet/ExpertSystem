from exceptions import ContradictionError

class Node:
    '''
    Attributes:
    label       : 'A', 'B', ... , 'Z'
    parents     : [ Node, ... ]
    children    : [ Node, ... ]
    value       : 'U' or 'True' or 'False' (default: 'False')

    Methods:
    addChildren : (children=[ Node, ... ]) => Node
    addParents  : (parents=[ Node, ... ])  => Node
    '''
    def __init__(self, label, verbose=False):
        self.children = []
        self.label = label
        self.parents = []
        self.value = 'False'
        self._set = False
        self.verbose = verbose
        if self.verbose:
            print("Node '" + label + "' created")

    def addChildren(self, *children):
        self.children += children
        return self

    def addParents(self, *parents):
        self.parents += parents
        return self

    def setValue(self, value):
        if self._set and self.value != value:
            raise ContradictionError('Two rules are in contradiction.')
        self._set = True
        self.value = value
        if self.verbose:
            print('Node', self.label, 'is now', self.value)
        return self.value

class Fact(Node):
    '''
    label   : 'A', 'B', ... , 'Z'

    example:
    children = [ Operator('AND') ]
    label   = 'A'
    parents = ( Operator('NOT'), None )
    value   = 'True'
    '''
    def __init__(self, label, verbose=False):
        super().__init__(label, verbose)

    def __repr__(self):
        return "Fact: label({}) value({})".format(self.label, self.value)

class Operator(Node):
    '''
    label   : 'NOT' || 'AND' || 'OR' || 'XOR' || 'IMP' || 'IFF'

    example:
    children = [ Operator('IMP') ]
    label   = 'AND'
    parents = ( Fact('A'), Fact('B') )
    value   = 'False'
    '''
    def __init__(self, label, verbose=False):
        super().__init__(label, verbose)

    def __repr__(self):
        return "Operator: label({}) value({})".format(self.label, self.value)
