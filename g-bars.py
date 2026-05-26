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

class GOBArgs(argparse.ArgumentParser):
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
        self.add_argument('--pfx', default='g-bar',
                          help='Prefix of output files '
                          'default:./g-agg')
        self.add_argument('--ext', default='.pdf',
                          help='Extension for files '
                          'default:.pdf')


def findmins(df):

    print('Minimum i-only data cache miss percentage for SFBest')

    bmarks = df['bmark'].unique()
    for b in bmarks:
        subf = df[df['bmark'] == b]
        subf = subf[subf['appr'] == common.BEST]
        subf = subf[subf['dmiss_iopct'] == subf['dmiss_iopct'].min()]
        print(subf[['bmark', 'appr', 'dmiss_iopct', 'cache_sets', 'blk_size', 'assoc']])

def bestp(ax, df, cache_sets, blk_size, assoc):
    subf = df[(df['cache_sets'] == cache_sets) &
              (df['blk_size'] == blk_size) &
              (df['assoc'] == assoc)]

    bmarks = subf['bmark'].unique()

    ionly = subf[subf['appr'] == common.IONLY]
    ionlyg = ionly.groupby('bmark')

    stack = subf[subf['appr'] == common.STACK]
    stackg = stack.groupby('bmark')

    best = subf[subf['appr'] == common.BEST]
    bestg = best.groupby('bmark')

    bargroups = len(bmarks)
    barpos = np.arange(bargroups)
    barwidth = .3

    ax.bar(barpos + (0 * barwidth), ionlyg['dmiss_iopct'].mean(), barwidth,
           color=appr2color(common.IONLY),
           label=appr2name(common.IONLY))
    ax.bar(barpos + (1 * barwidth), stackg['dmiss_iopct'].mean(), barwidth,
           color=appr2color(common.STACK),
           label=appr2name(common.STACK))
    ax.bar(barpos + (2 * barwidth), bestg['dmiss_iopct'].mean(), barwidth,
           color=appr2color(common.BEST),
           label=appr2name(common.BEST))

    ax.set_xticks(barpos + barwidth)
    ax.set_xticklabels(list(bestg.groups.keys()), rotation=45, ha='right')
    vals = ax.get_yticks()
    ax.set_yticks(vals)
    ax.set_yticklabels([f'{v}' r'\%' for v in vals])
    ax.set_xlabel('Benchmark')
    ax.set_ylabel('Percentage of ' + appr2name(common.IONLY) + '\nData Cache Misses')
    ax.legend(loc='lower right')

#
# Entry point
#
def main():
    argp = GOBArgs()
    parsed = argp.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f'Reading CSV {parsed.icsv}')
    df = pd.read_csv(parsed.icsv)

    opm = df[df['suite'] == 'openmp']

    fig, ax = plt.subplots()
    bestp(ax, opm, 16, 16, 1)

    fig.suptitle('Cache Sets: 16, Block Size: 16, Associativity: 1')
    fig.set_layout_engine('tight')

    fname = parsed.pfx + '.openmp' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    mrtc = df[df['suite'] == 'mrtc']
    findmins(mrtc)
    fig, ax = plt.subplots()
    sets = 16
    bsize = 16
    assoc = 1
    bestp(ax, mrtc, sets, bsize, assoc)
    fig.suptitle(f'Cache Sets: {sets}, Block Size: {bsize}, Associativity: {assoc}')
    fig.set_layout_engine('tight')
    fname = parsed.pfx + '.mrtc' + parsed.ext
    logger.info(f'Writing {fname}')
    fig.savefig(fname)
    fig.clear()
    plt.close()

    pass

if __name__ == '__main__':
    main()
