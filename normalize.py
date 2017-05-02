#!/usr/bin/python3

import sys
import unicodedata

def main():
  p_sp = re.compile(r'\s{2,}')
  for l in sys.stdin:
    ll = l.strip()
    ll = unicodedata.normalize('NFKC', ll)
    ll = p_sp.sub(' ', ll)
    print(ll)

if __name__ == '__main__':
  main()

