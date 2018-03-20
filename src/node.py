class Node:
    '''
    Attributes:
    children    : [ Node, ... ]
    label       : 'A', 'B', ... , 'Z'
    parents     : (Node, Node) || (Node, None) || (None, None)
    value       : 'U' or 'T' or 'F' (default: 'U')

    Methods:
    addChildren : (children=[ Node, ... ]) => Node
    setParents  : (parent1=Node, parent2=Node) => Node
    '''
    def __init__(self, label):
        self.children = []
        self.label = label
        self.parents = (None, None)
        self.value = 'U'
        print("Node '" + label + "' created")

    def addChildren(self, children=[]):
        self.children += children
        return self

    def setParents(self, parent1=None, parent2=None):
        self.parents = (parent1, parent2)
        return self


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