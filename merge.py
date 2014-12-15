#!/usr/bin/python3

import sys
import glob

def main():
    if len(sys.argv) != 2:
        print('usage: merge.py <file prefix>', file=sys.stderr)
        return

    prefix = sys.argv[1]

    fnames = sorted(glob.glob(prefix + '*'))
    if not fnames or prefix in fnames:
        print('invalid prefix: ' + prefix)
        return

    fps = [open(fn) for fn in fnames]

    with open(prefix, 'w') as fo:
        try:
            i = 0
            while True:
                line = next(fps[i])
                fo.write(line)
                i = (i + 1) % len(fnames)
        except StopIteration:
            pass

    for fp in fps:
        fp.close()

if __name__ == '__main__':
    main()

