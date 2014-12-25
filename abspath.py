#!/usr/bin/python3

import sys, os

for l in sys.argv[1:]:
    print(os.path.abspath(l))

