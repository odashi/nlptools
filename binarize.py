#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from util import sexpr


def binarize_left(tree):
    if isinstance(tree, str):
        return tree
    temp = [binarize_left(x) for x in tree]
    if len(temp) > 3:
        ch = binarize_left([('L#' if temp[0][:2] != 'L#' else '') + temp[0]] + temp[1:-1])
        temp = [temp[0], ch, temp[-1]]
    return temp


def binarize_right(tree):
    if isinstance(tree, str):
        return tree
    temp = [binarize_right(x) for x in tree]
    if len(temp) > 3:
        ch = binarize_right([('R#' if temp[0][:2] != 'R#' else '') + temp[0]] + temp[2:])
        temp = [temp[0], temp[1], ch]
    return temp


def main():
    if len(sys.argv) != 2:
        print('usage: binarize.py exp < input_parse', file=sys.stderr)
        print('  - exp: left | right', file=sys.stderr)
        return

    exp = sys.argv[1].lower()
    if exp == 'left':
        for l in sys.stdin:
            print(sexpr.encode(binarize_left(sexpr.decode(l))))
    elif exp == 'right':
        for l in sys.stdin:
            print(sexpr.encode(binarize_right(sexpr.decode(l))))
    else:
        print('invalid setting: exp=' + exp, file=sys.stderr)
    

if __name__ == '__main__':
    main()

