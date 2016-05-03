#!/usr/bin/python3

import sys

filenames = sys.argv[1:]
if not filenames:
  filenames.append('/dev/stdin')

for fn in filenames:
  words = set()
  with open(fn) as fp:
    for l in fp:
      for w in l.split():
        words.add(w)
  print('%s\t%d' % (fn, len(words)))

