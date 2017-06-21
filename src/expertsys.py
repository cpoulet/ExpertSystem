#!/usr/bin/env python3

import sys, string, re

symboles    = ['(',')','!','+','|','^','=>','<=>','=','?']
node_type   = ['fact', 'root', 'op_not', 'op_and', 'op_xor']
leafs       = []    #ugly
queries     = []    #ugly
knowledges  = []    #ugly

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
    for c in rule:
        if c in string.ascii_uppercase:
            leafs.append(c)
        else:
            print('Wrong initial facts')
    print('Leafs = ', leafs, sep=' ')
    return

def get_queries(rule):
    global queries  #ugly
    for c in rule:
        if c in string.ascii_uppercase:
            queries.append(c)
        else:
            print('Wrong queries')
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
    for rule in rules:
        if rule[0] == '=':
            get_leafs(rule[1:].strip())
        elif rule[0] == '?':
            get_queries(rule[1:].strip())
        else:
            rule = check_rule(rule)
            if rule[1] == '=>':
                knowledges.append((rule[0].strip(), rule[2].strip()))
            elif rule[1] == '<=>':
                knowledges.append((rule[0].strip(), rule[2].strip()))
                knowledges.append((rule[2].strip(), rule[0].strip()))
    print(*knowledges, sep='\n')
    return

class Nodes:

    def __init__(self, name = None,  ntype = node_type[0], children = None):
        self.ntype = ntype
        self.name = name if name else self.ntype
        self.children = []
        if children:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        try:
            assert (isinstance(node, Nodes), 'This node is not a Nodes')
            self.children.append(node)
        except NameError as e:
            print ("Error occurred :", e)

def create_tree(node):
    global knowledges
    global leafs
    print(node.name)

def solving_queries():
    global queries
    for querie in queries:
        root = Nodes(querie, 'root')
        create_tree(root)

def main(argv):
    if (len(argv) != 2):
        print ("Wrong number of arguments.")
        return
    try:
        text = open(argv[1], 'r').read()
        rules = remove_comment(text)
        knowledges = knowledge_base(rules)
        solving_queries()
    except FileNotFoundError as e:
        print ("Error occurred :", e)

if __name__ == "__main__":
   main(sys.argv)
