#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from util import sexpr


LEXTS = {
    'word': lambda x: x[1],
    'pos': lambda x: x[0],
    'lexicon': lambda x: x[1] + '/' + x[0]
}

def extract(tree, lext):
    if len(tree) == 2 and isinstance(tree[1], str):
        return [lext(tree)]
    else:
        ret = []
        for ch in tree[1:] if isinstance(tree[0], str) else tree:
            ret += extract(ch, lext)
        return ret


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
        print(' '.join(extract(sexpr.decode(l), lext)));


if __name__ == '__main__':
    main()

