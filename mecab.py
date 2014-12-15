#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser
from subprocess import check_output, Popen, PIPE


class MeCab:
    def __init__(self, path='', encoding='UTF-8'):
        self.__enc = encoding
        self.__path = path if path else check_output(['which', 'mecab']).decode(self.__enc).strip()

        command = [
            self.__path,
            '--input-buffer-size=100000',
        ]
        self.__proc = Popen(command, stdin=PIPE, stdout=PIPE)
        self.__obuf = iter(self.__proc.stdout)

    def tokenize(self, text):
        text = text.strip() + '\n'
        self.__proc.stdin.write(text.encode(self.__enc))
        ret = []
        while True:
            r = next(self.__obuf).decode(self.__enc).strip()
            if r == 'EOS':
                break
            r = r.split('\t')
            r[1] = tuple(r[1].split(','))
            ret.append(tuple(r))
        return ret


def parse_args():
    DEFAULT_INPUT = '/dev/stdin'
    DEFAULT_OUTPUT = '/dev/stdout'
    DEFAULT_MECAB_ENCODING = 'UTF-8'
    
    p = ArgumentParser()
    p.add_argument('--input', dest='input', default=DEFAULT_INPUT,
        help='input file (default: %s)' % DEFAULT_INPUT)
    p.add_argument('--output', dest='output', default=DEFAULT_OUTPUT,
        help='output file (default: %s)' % DEFAULT_OUTPUT)
    p.add_argument('--mecab-path', dest='mecab_path', default='',
        help='MeCab path (default: `which mecab`)')
    p.add_argument('--mecab-encoding', dest='mecab_encoding', default=DEFAULT_MECAB_ENCODING,
        help='MeCab encoding (default: %s)' % DEFAULT_MECAB_ENCODING)
    
    return p.parse_args()
    

def main():
    args = parse_args()
    mecab = MeCab(path=args.mecab_path, encoding=args.mecab_encoding)
    with open(args.input) as fi, open(args.output, 'w') as fo:
        for li in fi:
            for tok in mecab.tokenize(li):
                print(tok, file=fo)


if __name__ == '__main__':
    main()

