#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from nltk.tree import Tree


LEXTS = {
    'word': lambda x: x[1],
    'pos': lambda x: x[0],
    'lexicon': lambda x: x[1] + '/' + x[0]
}

def extract(tree):
    if isinstance(tree[0], str):
        yield (tree.label(), tree[0])
    else:
        for ch in tree:
            # yield from extract(ch)
            for ret in extract(ch):
                yield ret


def main():
    if len(sys.argv) != 2:
        print('usage: extract.py type < input_parse', file=sys.stderr)
        print('  - type: word | pos | lexicon', file=sys.stderr)
        return

    tp = sys.argv[1]
    try:
        lext = LEXTS[tp]
    except:
        print('invalid argument: type=' + tp, file=sys.stderr)
        return

    for l in sys.stdin:
        tree = Tree.fromstring(l)
        print(' '.join(lext(x) for x in extract(tree)))


if __name__ == '__main__':
    main()

