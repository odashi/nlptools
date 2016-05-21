#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) < 2:
  for l in sys.stdin:
    print(l.strip().lower())
else:
  for f in sys.argv[1:]:
    for l in open(f):
      print(l.strip().lower())

