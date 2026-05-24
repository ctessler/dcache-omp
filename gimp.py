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

IONLY='I-Only'
SFDBEST=r'I&D-SFBest'

# Argument parsing
import argparse
import csv
import logging

# data management and plotting
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class APArgs(argparse.ArgumentParser):
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
        self.add_argument('pfx', nargs='?', default='gimp-',
                          help='Name of the output file prefix '
                          'default:./gimp-')
        self.add_argument('ext', nargs='?', default='pdf',
                          help='Type of the output file '
                          'default:./pdf')

def appr2name(appr):
    fmts={IONLY   : 'I-Only',
          SFDBEST : r'I&D-SFBest'}

    return fmts[appr]

def mklabel(field):
    labels={
        'threads' : 'Threads',
        'cache_sets' : 'Cache Sets',
        'assoc' : 'Associativity',
        'dmiss' : 'Data Cache Misses',
        'dhit'  : 'Data Cache Hits',
        'imiss' : 'Instruction Cache Misses',
        'ihit'  : 'Instructio Cache Hits',
        'dmratio' : 'Data Cache Miss Ratio',
        'dhratio' : 'Data Cache Hit Ratio',
        'imratio' : 'Instruction Cache Miss Ratio',
        'ihratio' : 'Instruction Cache Hit Ratio',
        'tmratio' : 'Miss Ratio',
        'thratio' : 'Hit Ratio',
        'obs' : 'Observed Execution Cycles',
        'dmiss_iodif' : 'Data Cache Miss Reduction (v I-Only)',
        'dmiss_iopct' : r'Data Cache Misses (\% of I-Only)',
        'dhit_iodif'  : 'Data Cache Hit Reduction (v I-Only)',
        'dhit_iopct'  : r'Data Cache Hit (\% of I-Only)',
        'imiss_iodif' : 'Instruction Cache Miss Reduction (v I-Only)',
        'imiss_iopct' : r'Instruction Cache Misses (\% of I-Only)',
        'ihit_iodif'  : 'Instruction Cache Hit Reduction (v I-Only)',
        'ihit_iopct'  : r'Instruction Cache Hit (\% of I-Only)',
        'obs_iodif' : 'Observed Exection Time Reduction (v I-Only)',
        'obs_iopct' : r'Observed Execution Time (\% of I-Only)',
        'dmratio_iodif' : 'Data Cache Miss Ratio Reduction (v I-Only)',
        'dmratio_iopct' : r'Data Cache Miss Ratio (\% of I-Only)',
        'dhratio_iodif' : 'Data Cache Hit Ratio Reduction (v I-Only)',
        'dhratio_iopct' : r'Data Cache Hit Ratio (\% of I-Only)',
        'imratio_iodif' : 'Instruction Cache Miss Ratio Reduction (v I-Only)',
        'imratio_iopct' : r'Instruction Cache Miss Ratio (\% of I-Only)',
        'ihratio_iodif' : 'Instruction Cache Hit Ratio Reduction (v I-Only)',
        'ihratio_iopct' : r'Instruction Cache Hit Ratio (\% of I-Only)',
        'tmratio_iodif' : 'Cache Miss Ratio Reduction (v I-Only)',
        'tmratio_iopct' : r'Cache Miss Ratio (\% of I-Only)',
        'thratio_iodif' : 'Cache Hit Ratio Reduction (v I-Only)',
        'thratio_iopct' : r'Cache Hit Ratio (\% of I-Only)'
    }
    return labels[field]

def linear(df, parsed, appr, x, y):
    fig = _linear(df, appr, x, y)
    fname = parsed.pfx + f'{x}.{y}.' + parsed.ext
    logging.info(f'Writing {fname}')
    fig.savefig(fname, bbox_inches='tight')
    fig.clear()

def _linear(df, appr, x, y):
    fig, ax = plt.subplots()

    xlabel = mklabel(x)
    ylabel = mklabel(y)

    bmarks = df.bmark.unique()
    subf = df[df['appr'] == appr]

    groups = subf.groupby(['bmark'], group_keys=True)
    for key, groupf in groups:
        xvals = sorted(list(map(int, groupf[x].unique())))
        data = []
        for xval in xvals:
            avg = groupf[groupf[x] == xval][y].mean()
            data.append(avg)
        ax.plot(xvals, data, label=key[0])

    ax.set_xscale('symlog', base=2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(bbox_to_anchor=(1.0, 1.0))

    import matplotlib.ticker
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())

    return fig

#
# Entry point
#
def main():
    argp = APArgs()
    parsed = argp.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f'Reading CSV {parsed.icsv}')
    df = pd.read_csv(parsed.icsv)

    for x in ['threads', 'cache_sets', 'assoc']:
        for y in ['obs_iodif', 'obs_iopct',
                  'dmiss_iodif', 'dmiss_iopct']:
            linear(df, parsed, SFDBEST, x, y)

if __name__ == '__main__':
    main()
