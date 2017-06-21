#!/usr/bin/env python3

import sys, string, re

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

def main(argv):
    global queries
    global verbose
    if (len(argv) not in [2, 3]):
        print ("Wrong number of arguments.")
        return
    if '-v' in argv :
        verbose = 1
        argv.remove('-v')
        print('Verbosity activated')
    try:
        text = open(argv[1], 'r').read()
        rules = remove_comment(text)
        knowledges = knowledge_base(rules)
        for querie in queries:
            solving_querie(querie)
    except FileNotFoundError as e:
        print ("Error occurred :", e)

if __name__ == "__main__":
   main(sys.argv)
