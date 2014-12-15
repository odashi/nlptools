#!/usr/bin/python2
# -*- coding: utf-8 -*-


from __future__ import print_function
import sys
import numpy as np
import matplotlib.pylab as plt
from optparse import OptionParser


def trace(text, file=sys.stdout):
    print('show_align: ' + text, file=file)


def traceerr(text):
    trace('error: ' + text, file=sys.stderr)


def show_align(args):
    fname_corpus_f = args.fpath
    fname_corpus_e = args.epath
    fname_alignment = args.align
    sent_id = args.sent_id

    with open(fname_corpus_f) as fp_f, open(fname_corpus_e) as fp_e, open(fname_alignment) as fp_a:
        for _ in range(sent_id):
            toks_f = next(fp_f).decode('UTF-8')
            toks_e = next(fp_e).decode('UTF-8')
            alignment = next(fp_a)
        toks_f = toks_f.split()
        toks_e = toks_e.split()
        alignment = [tuple(int(aa) for aa in a.split('-')) for a in alignment.split()]

    trace('[f] = ' + ' '.join(toks_f))
    trace('[e] = ' + ' '.join(toks_e))
    trace('[a] = ' + ' '.join(str(x[0]) + '_' + str(x[1]) for x in alignment))

    lf = len(toks_f)
    le = len(toks_e)
    mwf = max(len(w) for w in toks_f)
    mwe = max(len(w) for w in toks_e)

    UNIT = 0.3 # inch
    PADDING = 0.5 # coord

    COLOR_LINE1 = '#000000'
    COLOR_LINE2 = '#882222'
    COLOR_LINE3 = '#77aa88'
    COLOR_LINE4 = '#333333'
    COLOR_FILL = '#3355bb'

    fontsize = 72.0 * UNIT * 0.8
    trace('fontsize = %f' % fontsize)

    WIDTH = max(6.4, UNIT * (lf+mwf+1))
    HEIGHT = max(4.8, UNIT * (le+mwe+1))

    plt.figure(figsize=(WIDTH, HEIGHT))
    ax = plt.gca()

    plt.xticks([])
    plt.yticks([])
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

    plt.axis([-mwf, lf, 0, le+mwe])
    plt.axis('equal')
    plt.fill( \
        [-mwf-PADDING, lf+PADDING, lf+PADDING, -mwf-PADDING], \
        [-PADDING, -PADDING, le+mwe+PADDING, le+mwe+PADDING], \
        facecolor='#ffffff', edgecolor='none', zorder=-1)

    def getstyle(x):
        if x % 5:
            return COLOR_LINE3, ':'
        else:
            return COLOR_LINE2, ':'

    # texts
    for x, wf in enumerate(toks_f):
        plt.text(x+0.5, le+0.5, wf,
            fontsize=fontsize,
            rotation='vertical',
            horizontalalignment='center',
            verticalalignment='bottom',
            zorder=0)
    for y, we in enumerate(toks_e):
        yy = le-y-1
        plt.text(-0.5, yy+0.5, we,
            fontsize=fontsize,
            horizontalalignment='right',
            verticalalignment='center',
            zorder=0)
    
    # borders
    for x in range(1, lf):
        color, linestyle = getstyle(x)
        plt.plot([x, x], [0, le], color=color, linestyle=linestyle, zorder=1)
    for y in range(1, le):
        yy = le-y
        color, linestyle = getstyle(y)
        plt.plot([0, lf], [yy, yy], color=color, linestyle=linestyle, zorder=1)
    plt.plot([0, 0], [0, le], COLOR_LINE1, zorder=3)
    plt.plot([lf, lf], [0, le], COLOR_LINE1, zorder=3)
    plt.plot([0, lf], [0, 0], COLOR_LINE1, zorder=3)
    plt.plot([0, lf], [le, le], COLOR_LINE1, zorder=3)
    
    # boxes
    for af, ae in alignment:
        yy=le-ae-1
        X = [af, af+1, af+1, af]
        Y = [yy, yy, yy+1, yy+1]
        plt.fill(X, Y, facecolor=COLOR_FILL, edgecolor=COLOR_LINE4, zorder=2)

    plt.show()


def parse_args():
    p = OptionParser(version='0.1 (2014/8/1)', usage='show_align fpath epath align sent_id')
    
    args, remain = p.parse_args()

    if len(remain) != 4:
        p.print_usage(file=sys.stderr)
        print('show_align: error: invalid number of arguments', file=sys.stderr)
        sys.exit()
    try:
        setattr(args, 'fpath', remain[0])
        setattr(args, 'epath', remain[1])
        setattr(args, 'align', remain[2])
        setattr(args, 'sent_id', int(remain[3]))
    except Exception as ex:
        p.print_usage(file=sys.stderr)
        print('show_align', file=sus.stderr)

    return args


def main():
    args = parse_args()
    show_align(args)


if __name__ == '__main__':
    main()

