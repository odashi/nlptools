#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import re
import unicodedata
from argparse import ArgumentParser


UNHAPPY_CHARS = {
    '<': '-LT-',
    '>': '-GT-',
    '(': '-LRB-',
    ')': '-RRB-',
    '{': '-LCB-',
    '}': '-RCB-',
    '[': '-LSB-',
    ']': '-RSB-',
}


# trim and normalize spaces
def normalize_spaces(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


# replace unhappy chars 
def replace_chars(text):
    global UNHAPPY_CHARS
    ret = ''
    for w in text:
        if w in UNHAPPY_CHARS:
            ret += UNHAPPY_CHARS[w]
        else:
            ret += w
    return ret


# check #words in the text
def check_length(text_f, text_e, args):
    lf = len(text_f.split())
    le = len(text_e.split())
    if lf < args.n_min: return False
    if le < args.n_min: return False
    if lf > args.n_max: return False
    if lf > args.n_max: return False
    r = max(lf/le, le/lf)
    if r > args.ratio: return False
    return True


def parse_args():
    DEFAULT_N_MIN = 1
    DEFAULT_N_MAX = 80
    DEFAULT_RATIO = 9.0

    p = ArgumentParser(version='0.2 (2014/8/6)')

    p.add_argument('in1', help='input file 1')
    p.add_argument('in2', help='input file 2')
    p.add_argument('out1', help='output file 1')
    p.add_argument('out2', help='output file 2')
    p.add_argument('--min', dest='n_min', default=DEFAULT_N_MIN, metavar='INT', type=int,
        help='minimum #words per line (default: %d)' % DEFAULT_N_MIN)
    p.add_argument('--max', dest='n_max', default=DEFAULT_N_MAX, metavar='INT', type=int,
        help='maximum #words per line (default: %d)' % DEFAULT_N_MAX)
    p.add_argument('--ratio', dest='ratio', default=DEFAULT_RATIO, metavar='FLOAT', type=float,
        help='upper bound of the ratio between lengths of parallel sentence (default: %f)' % DEFAULT_RATIO)
    p.add_argument('--unicode', dest='unicode_normalize', action='store_true', default=True,
        help='run unicode normalization (default)')
    p.add_argument('--no-unicode', dest='unicode_normalize', action='store_false',
        help='never run unicode normalization')
    p.add_argument('--lowercase', dest='lowercase', action='store_true',
        help='run lowercasing')
    p.add_argument('--no-lowercase', dest='lowercase', action='store_false', default=False,
        help='never run lowercasing (default)')
    
    args = p.parse_args()
    
    # checking
    try:
        if (args.n_min < 1): raise ValueError('you must set --nmin >= 1')
        if (args.n_max < 1): raise ValueError('you must set --nmax >= 1')
        if (args.ratio < 1.0): raise ValueError('you must set --ratio >= 1.0')
        if (args.n_max < args.n_min): raise ValueError('you must set --nmax >= --nmin')
    except Exception as ex:
        p.print_usage(file=sys.stderr)
        sys.exit()

    return args


def main():
    args = parse_args()

    path_if = args.in1
    path_ie = args.in2
    path_of = args.out1
    path_oe = args.out2

    with \
        open(path_if, 'r') as fp_if, \
        open(path_ie, 'r') as fp_ie, \
        open(path_of, 'w') as fp_of, \
        open(path_oe, 'w') as fp_oe:
        stored = 0
        ignored = 0
        for text_f, text_e in zip(fp_if, fp_ie):
            if args.unicode_normalize:
                text_f = unicodedata.normalize('NFKC', text_f)
                text_e = unicodedata.normalize('NFKC', text_e)
            text_f = normalize_spaces(text_f)
            text_e = normalize_spaces(text_e)
            text_f = replace_chars(text_f)
            text_e = replace_chars(text_e)
            if args.lowercase:
                text_f = text_f.lower()
                text_e = text_e.lower()
            if check_length(text_f, text_e, args):
                fp_of.write(text_f + '\n')
                fp_oe.write(text_e + '\n')
                stored += 1
            else:
                ignored += 1
    

if __name__ == '__main__':
    main()

