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
        self.add_argument('outfile', nargs='?', default='g-openmp-agg.pdf',
                          help='Name of the output file '
                          'default:./g-openmp-agg.pdf')

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
            label=f'{appr2name(common.IONLY)} {field}')
    ax.plot(sizes, [float(stack[x]) for x in sizes],
            label=f'{appr2name(common.STACK)} {field}')
    ax.plot(sizes, [float(best[x]) for x in sizes],
            label=f'{appr2name(common.BEST)} {field}')


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

    gkeys = ['cache_sets', 'blk_size', 'assoc', 'appr']
    gkeys = ['bmark', 'appr']
    groups = omp.groupby(gkeys, group_keys=True)

    for keys,frame in groups:
        (bmark, appr) = keys
        dmissavg = round(frame['dmiss'].mean())
        dmisspct = round(frame['dmratio'].mean() * 100, 2)
        dmioavg = round(frame['dmiss_ionly'].mean())
        dmiopct = round(frame['dmiss_iopct'].mean(), 2)
        # print(f'{bmark} {appr} Data Miss {dmissavg}({dmisspct}%) pct I-Only ({dmioavg}){dmiopct}%')

    # Get the unique cache sizes
    sizes = []
    groups = omp.groupby(['cache_sets', 'blk_size', 'assoc'], group_keys=True)
    for keys,frame in groups:
        (s, b, a) = keys
        sizes.append(s * b * a)
    sizes = sorted(list(set(sizes)))

    # Get the values per cache size
    gkeys = ['cache_sets', 'blk_size', 'assoc', 'appr']
    groups = omp.groupby(gkeys, group_keys=True)
    ionly = {}
    stack = {}
    best  = {}
    for a,b in groups:
        (sets, blk, assoc, appr) = a
        size = sets * blk * assoc

        dmisspct = round((100 - b['dmiss_iopct'].mean()), 2)
        if appr == common.IONLY:
            ionly[size] = dmisspct
        elif appr == common.STACK:
            stack[size] = dmisspct
        elif appr == common.BEST:
            best[size] = dmisspct
        else:
            raise ValueError

    bargroups = len(sizes)
    barpos = np.arange(bargroups)
    barwidth = .3
    fig, ax = plt.subplots()


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

    ax.set_ylabel('Data Cache Miss Improvement Compared to I-Only')
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

    fig.suptitle('OpenMP Benchmarks')
    fig.set_layout_engine('compressed')
    fig.savefig(parsed.outfile)
    fig.clear()

    fig, ax = plt.subplots()
    threepack(omp, sizes, 'dmiss_iopct', ax, 'dmiss_iopct')
    threepack(omp, sizes, 'imiss_iopct', ax, 'imiss_iopct')
    threepack(omp, sizes, 'tmiss_iopct', ax, 'tmiss_iopct')
    ax.legend()
    # fig.savefig('test2.pdf')
    # fig.clear()

if __name__ == '__main__':
    main()
