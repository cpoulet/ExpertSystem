#!/usr/bin/env python3

import argparse
import os
import sys

from exceptions import InputError
from expertsys import Expertsystem

def main():
    parser = argparse.ArgumentParser(description='Read a Knowledge base then answer the queries.')
    parser.add_argument('input', action='store', help='Input file describing the rules.')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    if not os.path.exists(args.input) or not os.path.isfile(args.input):
        raise InputError('File not found: "' + args.input + '".')
    e = Expertsystem(args.verbose)
    e.parseFile(args.input)
    e.answerQueries()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error : ' + str(e))
