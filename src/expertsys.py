#!/usr/bin/env python3

import argparse, re, os

symboles    = ['(',')','!','+','|','^','=>','<=>','=','?']
node_type   = ['fact', 'root', 'op_not', 'op_and', 'op_xor']
leafs       = []    #ugly
queries     = []    #ugly
knowledges  = []    #ugly
verbose     = 0

class Fact:
    def __init__(self, name, state = False):
        if (len(name) != 1 or not name in string.ascii_uppercase):
            print ("Wrong Fact name.")
            exit()
        self.name = name
        self.state = False

def rule_error():
    print ("Wrong rules")

def remove_comment(string):
    rules = []
    for line in string.split('\n'):
        rule, sep, comment = line.partition('#')
        if rule.strip():
            rules.append(rule)
    return rules

def get_leafs(rule):
    global leafs    #ugly
    global verbose
    for c in rule:
        if c in string.ascii_uppercase:
            leafs.append(c)
        else:
            print('Wrong initial facts')
    if verbose:
        print('Leafs = ', leafs, sep=' ')
    return

def get_queries(rule):
    global queries  #ugly
    global verbose
    for c in rule:
        if c in string.ascii_uppercase:
            queries.append(c)
        else:
            print('Wrong queries')
    if verbose:
        print('Queries = ', queries, sep=' ')
    return

def check_rule(rule):
    if rule.count('=>') >= 2 or bool(re.search(r'[^A-Z\s+|()!^=><]', rule)):
        rule_error()
        return [0, 0]   #moche
    else:
        return rule.partition('<=>' if rule.count('<=>') else '=>')

def knowledge_base(rules):
    global knowledges
    global verbose
    for rule in rules:
        if rule[0] == '=':
            get_leafs(rule[1:].strip())
        elif rule[0] == '?':
            get_queries(rule[1:].strip())
        else:
            rule = check_rule(rule)
            if rule[1] == '=>':
                knowledges.append([rule[0].strip(), rule[2].strip(), 1])
            elif rule[1] == '<=>':
                knowledges.append([rule[0].strip(), rule[2].strip(), 1])
                knowledges.append([rule[2].strip(), rule[0].strip(), 1])
    if verbose:
        print(*knowledges, sep='\n')
    return

class Nodes:

    def __init__(self, name = None,  ntype = node_type[0], children = None):
        self.ntype = ntype
        self.name = name if name else self.ntype
        self.children = []
        if children:
            for child in children:
                self.add_child(Nodes(child))
        if ntype == 'root':
            print('New tree created to answer ' + self.name + '?')

    def add_child(self, node):
        try:
            assert isinstance(node, Nodes), 'This node is not a Nodes'
            self.children.append(node)
        except NameError as e:
            print (e)

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
        return ret

    def p_prefix(self):
        print (self.name)
        for child in self.children:
            child.p_prefix()

    def p_suffix(self):
        for child in self.children:
            child.p_suffix()
        print (self.name, end=(' ' if self.ntype != 'root' else '\n')) #ugly

def evaluate(expr):
   pass

def grow_tree(node, goal):
    global leafs
    global knowledges
    if goal in leafs:
        print('Leaf found')
        return
    symbols = [symbol for symbol in goal[0].split() if symbol in string.ascii_uppercase]
    for symbol in symbols:
        for goal in knowledges:
            print(goal)
            if goal[2] and symbol in goal[1]:   #problem with !X
                node.add_child(Nodes(symbol))
                goal[2] = 0
                grow_tree(node.children[-1], goal[0])

def solving_querie(querie):
    global knowledges
    global leafs
    root = Nodes(querie, 'root')
    for goal in knowledges:
        if querie in goal[1]:
            grow_tree(root, goal)
            root.p_breadth()

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
                        raise Exception('Parsing error : Wrong initial facts')
                    self._leafs = list(l[1:])

                elif l[0] == '?':
                    if re.search(r'[^A-Z]', l[1:]):
                        raise Exception('Parsing error : Wrong queries')
                    self._queries = list(l[1:])

                else:
                    s = re.search(r'(^[A-Z+|()!^]+)(<?)=>([A-Z+|()!^]+$)', l)
                    if not s:
                        raise Exception('Parsing error : Wrong rules')
                    self._knowledges.append([s.group(1), s.group(3)])
                    if s.group(2):
                        self._knowledges.append([s.group(3), s.group(1)])

        if self._verbose:
            print('Leafs = ' + str(self._leafs))
            print('Queries = ' + str(self._queries))
            print(*self._knowledges, sep='\n')

def main():
    parser = argparse.ArgumentParser(description='Read a Knowledge base then answer the queries.')
    parser.add_argument('input_', action='store', help='Input file describing the rules.')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    if not os.path.exists(args.input_) or not os.path.isfile(args.input_):
        raise Exception('File not found: "' + args.input_ + '".')
    e = Expertsystem(args.verbose)
    e.parse_file(args.input_)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error : ' + str(e))
