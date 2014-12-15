# -*- coding: utf-8 -*-

import re
import sys


def decode(text):
    toks = [x for x in re.sub(r'([()])', r' \1 ', text).split() if x];
    stack = []

    for w in toks:
        if w == ')':
            tree = []
            while stack[-1] != '(':
                tree.insert(0, stack.pop())
            stack[-1] = tree
        else:
            stack.append(w)

    return stack[-1]


def encode(tree):
    if isinstance(tree, str):
        return tree
    else:
        return '(' + ' '.join(encode(x) for x in tree) + ')'

