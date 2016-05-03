#!/usr/bin/python3

import math
import sys
from argparse import ArgumentParser

def parse_args():
  p = ArgumentParser(
    description='Corpus stats collector',
    usage='%(prog)s [flags] [corpus-list]',
  )

  p.add_argument(
    'corpus',
    type=str, metavar='STR', nargs='*',
    help='target corpus')

  return p.parse_args()

def main(args):
  if not args.corpus:
    args.corpus.append('/dev/stdin')

  for fn in args.corpus:
    num_sents = 0
    min_len = 1000000
    max_len = -1
    total_len = 0
    total_sq_len = 0
    vocab = set()

    with open(fn) as fp:
      for sent in fp:
        sent = sent.split()
        sent_len = len(sent)

        num_sents += 1
        if sent_len < min_len: min_len = sent_len
        if sent_len > max_len: max_len = sent_len
        total_len += sent_len
        total_sq_len += sent_len * sent_len

        for w in sent:
          vocab.add(w)

    mean = total_len / num_sents
    sd = math.sqrt(total_sq_len / num_sents - mean * mean)
    print('%s:' % fn)
    print('  #sentences:     %7d' % num_sents)
    print('  min length:     %7d' % min_len)
    print('  max length:     %7d' % max_len)
    print('  average length: %11.3f' % mean)
    print('  SD of length:   %11.3f' % sd)
    print('  #vocaburaly:    %7d' % len(vocab))
    print()

if __name__ == '__main__':
  args = parse_args()
  main(args)
