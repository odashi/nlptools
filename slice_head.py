#!/usr/bin/python3
import sys

def main():
  if len(sys.argv) != 3:
    print('usage: python slice-head.py [N] [FILE1] < INPUT > FILE2', file=sys.stderr)
    return

  N = int(sys.argv[1])
  if N < 0:
    N = -N # '-12345' should be 12345

  # slice head lines
  try:
    with open(sys.argv[2], 'w') as fp:
      for i in range(N):
        fp.write(next(sys.stdin))
  except:
    pass
  
  # remaining
  for line in sys.stdin:
    sys.stdout.write(line)
  
if __name__ == '__main__':
  main()
