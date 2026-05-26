#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
# Please format with autopep8
#
# Local Variables:
# mode: Python
# eval: (auto-fill-mode)
# fill-column: 79
# End:

# Argument parsing
import argparse
import csv
import logging

# data management and plotting
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import common
from common import appr2name, appr2color, appr2line, appr2mark

class GOAArgs(argparse.ArgumentParser):
    '''Parses the command line arguments'''

    desc = '''
    Given a list of CSV file describing results from the run, compile them into
    a single CSV
    '''

    def __init__(self):
        super().__init__(
            description=self.desc,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        self.add_argument('icsv', nargs='?', help='Input CSV file')
        self.add_argument('--pfx', default='g-agg-',
                          help='Prefix of output files '
                          'default:./g-agg')
        self.add_argument('--ext', default='.pdf',
                          help='Extension for files '
                          'default:.pdf')

def _3pack(subf, ax, x, xlabel, y, ylabel, dopct=False):
    ionly = {}
    stack = {}
    best  = {}

    groups = subf.groupby([x, 'appr'])
    xvals = sorted(subf[x].unique())
    for keys,frame in groups:
        (k, appr) = keys
        if appr == common.IONLY:
            ionly[k] = frame[y].mean()
        if appr == common.STACK:
            stack[k] = frame[y].mean()
        if appr == common.BEST:
            best[k] = frame[y].mean()

    ax.plot(xvals, [float(ionly[v]) for v in xvals],
            label=appr2name(common.IONLY),
            linestyle=appr2line(common.IONLY),
            marker=appr2mark(common.IONLY),
            color=appr2color(common.IONLY))
    ax.plot(xvals, [float(stack[v]) for v in xvals],
            label=appr2name(common.STACK),
            linestyle=appr2line(common.STACK),
            marker=appr2mark(common.STACK),
            color=appr2color(common.STACK))
    ax.plot(xvals, [float(best[v]) for v in xvals],
            label=appr2name(common.BEST),
            linestyle=appr2line(common.BEST),
            marker=appr2mark(common.BEST),
            color=appr2color(common.BEST))

    ax.set_xscale('log', base=2)
    ax.set_xticks(xvals)
    if dopct:
        vals = ax.get_yticks()
        ax.set_yticks(vals)
        ax.set_yticklabels([f'{v}' r'\%' for v in vals])

    ax.set_xticklabels(xvals)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()

def threepack(subf, sizes, field, ax, label):
    ionly = {}
    stack = {}
    best  = {}

    gkeys = ['cache_sets', 'blk_size', 'assoc', 'appr']
    groups = subf.groupby(gkeys, group_keys=True)
    for a,b in groups:
        (sets, blk, assoc, appr) = a
        size = sets * blk * assoc

        dmisspct = round((100 - b[field].mean()), 2)
        if appr == common.IONLY:
            ionly[size] = dmisspct
        elif appr == common.STACK:
            stack[size] = dmisspct
        elif appr == common.BEST:
            best[size] = dmisspct
        else:
            raise ValueError

    ax.plot(sizes, [float(ionly[x]) for x in sizes],
            label=appr2name(common.IONLY),
            linestyle=appr2line(common.IONLY),
            marker=appr2mark(common.IONLY),
            color=appr2color(common.IONLY))
    ax.plot(sizes, [float(stack[x]) for x in sizes],
            label=appr2name(common.STACK),
            linestyle=appr2line(common.STACK),
            marker=appr2mark(common.STACK),
            color=appr2color(common.STACK))
    ax.plot(sizes, [float(best[x]) for x in sizes],
            label=appr2name(common.BEST),
            linestyle=appr2line(common.BEST),
            marker=appr2mark(common.BEST),
            color=appr2color(common.BEST))


    if label == 'dmiss_iopct':
        metric = 'Data'
    else:
        metric = 'Total'

    ax.set_ylabel(f'{metric} Cache Miss Improvement Compared to I-Only')
    ax.set_xlabel('Cache Size (Bytes)')
    ax.set_xscale('log', base=2)
    ax.set_xticks(sizes)

    vals = ax.get_yticks()
    ax.set_yticks(vals)
    ax.set_yticklabels([f'{v}' r'\%' for v in vals])
    ax.legend()

    import matplotlib.ticker
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())

#
# Entry point
#
def main():
    argp = GOAArgs()
    parsed = argp.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f'Reading CSV {parsed.icsv}')
    df = pd.read_csv(parsed.icsv)

    omp = df[df['suite'] == 'openmp']
    mrtc = df[df['suite'] == 'mrtc']

    # Get the unique cache sizes
    sizes = []
    groups = omp.groupby(['cache_sets', 'blk_size', 'assoc'], group_keys=True)
    for keys,frame in groups:
        (s, b, a) = keys
        sizes.append(s * b * a)
    sizes = sorted(list(set(sizes)))


    #
    # OpenMP threads vs dmiss_iopct
    #
    fig, ax = plt.subplots()
    _3pack(omp, ax, 'threads', 'Threads', 'dmiss_iopct',
           'Percentage of I-Only Data Cache Misses', dopct=True)
    fig.set_layout_engine('compressed')
    fname = parsed.pfx + 'threads.dmiss_iopct.openmp' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    #
    # OpenMP associativity vs dmiss_iopct
    #
    fig, ax = plt.subplots()
    _3pack(omp, ax, 'assoc', 'Associativity', 'dmiss_iopct',
           'Percentage of I-Only Data Cache Misses', dopct=True)
    fig.set_layout_engine('compressed')
    fname = parsed.pfx + 'assoc.dmiss_iopct.openmp' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    #
    # OpenMP associativity vs dmiss_iopct
    #
    fig, ax = plt.subplots()
    _3pack(omp, ax, 'blk_size', 'Block Size', 'dmiss_iopct',
           'Percentage of I-Only Data Cache Misses', dopct=True)
    fig.set_layout_engine('compressed')
    fname = parsed.pfx + 'bsize.dmiss_iopct.openmp' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    #
    # OpenMP data cache misses
    #
    fig, ax = plt.subplots()
    threepack(omp, sizes, 'dmiss_iopct', ax, 'dmiss_iopct')
    fig.suptitle('OpenMP Benchmarks')
    fig.set_layout_engine('compressed')
    fname = parsed.pfx + 'dmiss_iopct.openmp' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    #
    # OpenMP total cache misses
    #
    fig, ax = plt.subplots()
    threepack(omp, sizes, 'tmiss_iopct', ax, 'tmiss_iopct')
    fig.suptitle('OpenMP Benchmarks')
    fig.set_layout_engine('compressed')
    fname = parsed.pfx + 'tmiss_iopct.openmp' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    #
    # MRTC data cache misses
    #
    fig, ax = plt.subplots()
    threepack(mrtc, sizes, 'dmiss_iopct', ax, 'dmiss_iopct')
    fig.suptitle('MRTC Benchmarks')
    fig.set_layout_engine('compressed')
    fname = parsed.pfx + 'dmiss_iopct.mrtc' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    #
    # MRTC total cache misses
    #
    fig, ax = plt.subplots()
    threepack(mrtc, sizes, 'tmiss_iopct', ax, 'tmiss_iopct')
    fig.suptitle('MRTC Benchmarks')
    fig.set_layout_engine('compressed')
    fname = parsed.pfx + 'tmiss_iopct.mrtc' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

if __name__ == '__main__':
    main()
