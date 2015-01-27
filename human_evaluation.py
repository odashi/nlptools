#!/usr/bin/python3

import sys
import argparse
import os
import random


def getargs():
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''Human Evaluation Script v0.1 by Odashi

example:
    human_evaluation.py
        --src test.fr
        --ref ref1.en ref2.en ref3.en
        --hyp hyp1.en hyp2.en hyp3.en
        --out result.tsv
        --measure Adequecy Fluency
        --min-level 1 1
        --max-level 5 5
        --skip 0
        --num 100
''')
    p.add_argument('--src',
                   required=False, metavar='PATH', type=str, default='',
                   help='source corpora')
    p.add_argument('--ref',
                   required=False, metavar='PATH', type=str, nargs='+', default=[],
                   help='reference corpus')
    p.add_argument('--hyp',
                   required=True, metavar='PATH', type=str, nargs='+',
                   help='hypothesis corpus')
    p.add_argument('--out',
                   required=True, metavar='PATH', type=str,
                   help='evaluation results')
    p.add_argument('--measure',
                   required=True, metavar='STR', type=str, nargs='+',
                   help='names of evaluation measure')
    p.add_argument('--min-level',
                   required=True, metavar='INT', type=int, nargs='+',
                   help='minimum numbers of evaluation measure')
    p.add_argument('--max-level',
                   required=True, metavar='INT', type=int, nargs='+',
                   help='maximum numbers of evaluation measure')
    p.add_argument('--skip',
                   required=False, metavar='INT', type=int, default=0,
                   help='number of skipping sentences')
    p.add_argument('--num',
                   required=False, metavar='INT', type=int, default=0,
                   help='number of evaluating sentences (0: all sentences)')
    return p.parse_args()


def checkargs(args):
    if args.src and not os.path.exists(args.src):
        raise RuntimeError('file not found: ' + args.src)
    for f in args.ref:
        if not os.path.exists(f):
            raise RuntimeError('file not found: ' + f)
    for f in args.hyp:
        if not os.path.exists(f):
            raise RuntimeError('file not found: ' + f)
    if len(args.min_level) != len(args.measure):
        raise RuntimeError('num of --measure and --min-level must be same')
    if len(args.max_level) != len(args.measure):
        raise RuntimeError('num of --measure and --max-level must be same')
    for i in range(len(args.measure)):
        if args.min_level[i] >= args.max_level[i]:
            raise RuntimeError('--min-level must be lower than --max-level')
    if args.skip < 0:
        raise RuntimeError('--skip must be 0 or positive')
    if args.num < 0:
        raise RuntimeError('--num must be 0 or positive')


def getscore(name, lmin, lmax):
    p = True
    ret = -1
    while p:
        p = False
        try:
            ret = int(input('%s [%d..%d] > ' % (name, lmin, lmax)))
            if ret < lmin or ret > lmax:
                p = True
        except Exception:
            p = True
    return ret


def main():
    args = getargs()
    checkargs(args)

    corpus_src = [x.strip() for x in open(args.src)] if args.src else None
    corpus_ref = [[x.strip() for x in open(f)] for f in args.ref]
    corpus_hyp = [[x.strip() for x in open(f)] for f in args.hyp]

    N = len(corpus_hyp[0])
    H = len(corpus_hyp)
    R = len(corpus_ref)

    for i in range(H):
        if len(corpus_hyp[i]) != N:
            raise RuntimeError('corpus size are different')
    if args.skip >= N:
        raise RuntimeError('--skip is too large')

    begin = args.skip
    end = min(N, begin + args.num) if args.num > 0 else N
    NN = end - begin

    corpus_src = corpus_src[begin:end] if corpus_src else None
    corpus_ref = [x[begin:end] for x in corpus_ref]
    corpus_hyp = [x[begin:end] for x in corpus_hyp]

    order = []
    for h in range(H):
        order += [(h, n) for n in range(NN)]
    random.shuffle(order)

    scores = {}

    for i, (h, n) in enumerate(order):
        print()
        print('================================================================')
        #print('hypothesis %d, sentence %d:' % (k+1, begin+n+1))
        print('[Sample %d]' % (i+1))
        print()
        print('----------------------------------------------------------------')
        if corpus_src:
            print('Source:')
            print(corpus_src[n])
            print()
            print('----------------------------------------------------------------')
        for r in range(R):
            print('Reference %d:' % (r+1))
            print(corpus_ref[r][n])
            print()
            print('----------------------------------------------------------------')
        print('Hypothesis:')
        print(corpus_hyp[h][n])
        print()
        print('----------------------------------------------------------------')
        for name, lmin, lmax in zip(args.measure, args.min_level, args.max_level):
            scores[name, h, n] = getscore(name, lmin, lmax)

    print()
    print('Finish!')
    print()
    
    with open(args.out, 'w') as fp:
        for name in args.measure:
            print(name + ':', file=fp)
            print('Sentence\t' + '\t'.join(args.hyp), file=fp)
            for n in range(NN):
                print(str(begin+n+1) + '\t' + '\t'.join((str(scores[name, h, n]) for h in range(H))), file=fp)
            print(file=fp)



if __name__ == '__main__':
    main()


