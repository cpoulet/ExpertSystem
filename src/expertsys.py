#!/usr/bin/env python3

import sys, string

symboles = ['(',')','!','+','|','^','=>','<=>','=','?']
leafs = []
queries = []

class Fact():
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
	global leafs
	for c in rule:
		if c in string.ascii_uppercase:
			leafs.append(c)
		else:
			print('Wrong initial facts')
	print(leafs)
	return

def get_queries(rule):
	global queries
	for c in rule:
		if c in string.ascii_uppercase:
			queries.append(c)
		else:
			print('Wrong queries')
	print(queries)
	return

def check_rule(rule):
	if rule.count('=>') >= 2:
		rule_error()
	else:
		rule = rule.partition('<=>' if rule.count('<=>') else '=>')
		print(rule)

def knowledge_base(rules):
	for rule in rules:
		if rule[0] == '=':
			get_leafs(rule[1:].strip())
		elif rule[0] == '?':
			get_queries(rule[1:].strip())
		else:
			check_rule(rule)

def main(argv):
	if (len(argv) != 2):
		print ("Wrong number of arguments.")
		return
	try:
		text = open(argv[1], 'r').read()
		rules = remove_comment(text)
		knowledge_base(rules)
	except FileNotFoundError as e:
		print ("Error occurred :", e)

if __name__ == "__main__":
   main(sys.argv)
