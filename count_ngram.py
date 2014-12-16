#!/usr/bin/python3

import sys
from collections import defaultdict


def main():
    if len(sys.argv) != 2:
        print('usage: count_ngram.py N < input_toks', file=sys.stderr)
        print('  - N: length of n-gram (1 <= N <= 7)', file=sys.stderr)
        return

    N = int(sys.argv[1])
    if N < 1 or N > 7:
        print('ERROR: N must be (1 <= N <= 7)', file=sys.stderr)
        return

    freq = defaultdict(lambda: 0)

    for l in sys.stdin:
        ls = l.split()
        for i in range(len(ls) - N + 1):
            freq[tuple(ls[i : i + N])] += 1

    for k, v in freq.items():
        print('%s\t%d' % (' '.join(k), v))


if __name__ == '__main__':
    main()


