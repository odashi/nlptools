#!/usr/bin/python3

import sys
import unicodedata

for l in sys.stdin:
    print(unicodedata.normalize('NFKC', l.strip()))

