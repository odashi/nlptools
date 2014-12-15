#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from nltk.tree import Tree

def show_gui():
    line = next(iter(sys.stdin)).strip()
    t = Tree.fromstring(line)
    t.draw()

def show_text():
    def recursive(tree, depth):
        #print('"%s [%d]"' % (tree, depth))
        if isinstance(tree, Tree):
            if depth > 0:
                print()
            print('    ' * depth + '(' + tree.label() + ' ', end='')
            for ch in tree:
                recursive(ch, depth + 1)
            print(')', end=('\n' if depth == 0 else ''))
        else:
            print(str(tree), end='')

    line = next(iter(sys.stdin)).strip()
    t = Tree.fromstring(line)
    recursive(t, 0)

if __name__ == '__main__':
    if '--gui' in sys.argv:
        show_gui()
    else:
        show_text()

