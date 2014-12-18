#!/usr/bin/python3

import sys
import random
from argparse import ArgumentParser


def trace(text, file=sys.stdout):
    print('make_crossvalid: ' + text, file=file)

def traceerr(text):
    trace('error: ' + text, file=sys.stderr)


def parse_args():
    p = ArgumentParser()
    p.add_argument('input', help='input corpus prefix')
    p.add_argument('output', help='output corpus prefix')
    p.add_argument('lf', help='source language suffix')
    p.add_argument('le', help='target language suffix')
    p.add_argument('n', type=int, help='number of division (2 to 100)')
    #p.add_argument('--shuffle', action='store_true', dest='shuffle', default=True,
    #    help='shuffle the order of sentence in the corpus (default)')
    #p.add_argument('--no-shuffle', action='store_false', dest='shuffle',
    #    help='keep the order of sentence in the corpus')

    args = p.parse_args()

    try:
        if args.n < 2: raise ValueError('n is too small. you must set n >= 2.')
        if args.n > 100: raise ValueError('n is too large. you must set n <= 100.')
    except Exception as ex:
        p.print_usage(file=sys.stderr)
        traceerr(str(ex))
        sys.exit()
    
    return args


def main():
    args = parse_args()

    path_if = args.input + '.' + args.lf
    path_ie = args.input + '.' + args.le
    path_of_tmp = args.output + '.%s%s.' + args.lf
    path_oe_tmp = args.output + '.%s%s.' + args.le

    with open(path_if) as fp:
        corpus_f = [l.strip() for l in fp]
    with open(path_ie) as fp:
        corpus_e = [l.strip() for l in fp]

    nf = len(corpus_f)
    ne = len(corpus_e)
    if nf != ne:
        traceerr('number of sentences mismatched: F=%d, E=%d' % (nf, ne))
        sys.exit()

    div = nf // args.n
    mod = nf % args.n
    nums = [div + (1 if x < mod else 0) for x in range(args.n)]

    for i in range(args.n):
        str_i = '%03d' % i
        path_of_train = path_of_tmp % (str_i, 'train')
        path_oe_train = path_oe_tmp % (str_i, 'train')
        path_of_test = path_of_tmp % (str_i, 'test')
        path_oe_test = path_oe_tmp % (str_i, 'test')
        num_train1 = sum(nums[:i])
        num_train2 = sum(nums[i+1:])
        num_test = nums[i]

        trace('%s.%s: train=%d, test=%d' % (args.output, str_i, num_train1+num_train2, num_test))

        with \
            open(path_of_train, 'w') as fp_of_train, \
            open(path_oe_train, 'w') as fp_oe_train, \
            open(path_of_test, 'w') as fp_of_test, \
            open(path_oe_test, 'w') as fp_oe_test:

            zipped = zip(corpus_f, corpus_e)

            for j in range(num_train1):
                sent_f, sent_e = next(zipped)
                fp_of_train.write(sent_f + '\n')
                fp_oe_train.write(sent_e + '\n')

            for j in range(num_test):
                sent_f, sent_e = next(zipped)
                fp_of_test.write(sent_f + '\n')
                fp_oe_test.write(sent_e + '\n')

            for j in range(num_train2):
                sent_f, sent_e = next(zipped)
                fp_of_train.write(sent_f + '\n')
                fp_oe_train.write(sent_e + '\n')


if __name__ == '__main__':
    main()

