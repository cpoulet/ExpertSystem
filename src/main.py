import sys

from exceptions import ArgumentError
from graph import GraphCreator

def main(argv):
    if len(argv) != 2:
        raise ArgumentError('Only one argument is needed.')
    e = GraphCreator()
    graph = e.parse('A + B => C')
    graph = e.parse('C | D => E', graph)

if __name__ == "__main__":
    try:
	    main(sys.argv)
    except Exception as e:
        print('Error : ' + str(e))
        '''
        A => B + C
        D => C
        '''
