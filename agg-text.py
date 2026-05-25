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
from common import appr2name, appr2color, appr2line

class ATArgs(argparse.ArgumentParser):
    '''Parses the command line arguments'''

    desc = '''
    Given a list of CSV file describing results from the run, compile them into
    a single CSV
    '''

    def __init__(self):
        super().__init__(
            description=self.desc,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        self.add_argument('--suite', type=str, default='mrtc',
                          help='The suite of benchmarks to get the data for'
                          ' (mrtc|openmp) default:mrtc')
        self.add_argument('--max-size', type=int, default=4096,
                          help='Limits the values output by maximum cache size'
                          ' default:4096')
        self.add_argument('icsv', nargs='?', help='Input CSV file')
        self.add_argument('outfile', nargs='?', default='agg-text-4096.txt',
                          help='Name of the compiled output file '
                          'default:./agg-text-4096.txt')

def apprvals(df, appr, ofile):
    print(f'{common.appr2name(appr):8s}'
          f'\t{round(df['dmiss'].mean())}'
          f'({(df['dmratio'].mean() * 100):.2f}%)'
          f'\t{round(df['imiss'].mean())}'
          f'({(df['imratio'].mean() * 100):.2f}%)'
          f'\t{round(df['tmiss'].mean())}'
          f'({(df['tmratio'].mean() * 100):.2f}%)',
          file=ofile)

def apprvio(df, appr, ofile):
    print(f'{common.appr2name(appr):8s}',
          f'\t{round(df['dmiss_iodif'].mean())}'
          f'({100 - df['dmiss_iopct'].mean():.2f}%)'
          f'\t{round(df['imiss_iodif'].mean())}'
          f'({100 - df['imiss_iopct'].mean():.2f}%)'
          f'\t{round(df['tmiss_iodif'].mean())}'
          f'({100 - df['tmiss_iopct'].mean():.2f}%)',
          file=ofile)

#
# Entry point
#
def main():
    argp = ATArgs()
    parsed = argp.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f'Reading CSV file {parsed.icsv}')
    df = pd.read_csv(parsed.icsv)

    df = df[df['suite'] == parsed.suite]
    df = df[(df['cache_sets'] * df['blk_size'] * df['assoc']) <= parsed.max_size]

    ionly = df[df['appr'] == common.IONLY]
    stack = df[df['appr'] == common.STACK]
    best  = df[df['appr'] == common.BEST]

    with open(parsed.outfile, 'w') as ofile:
        print(f' ' * 30 + 'Raw Values', file=ofile)
        print(f'Approach\tAvg. dmiss \tAvg. imiss \tAvg. miss', file=ofile)
        print(f'        \tcount(pct) \tcount(pct) \tcount(pct)', file=ofile)
        print('-' * 60, file=ofile)
        apprvals(ionly, common.IONLY, ofile)
        apprvals(stack, common.STACK, ofile)
        apprvals(best, common.BEST, ofile)

        print(f'\n\n', file=ofile)
        print(f' ' * 30 + 'Comparison to I-Only', file=ofile)
        print(f'Approach\tAvg. dmiss \tAvg. imiss \tAvg. miss', file=ofile)
        print(f'        \treduction  \treduction  \treduction', file=ofile)
        print(f'        \tcount(pct) \tcount(pct) \tcount(pct)', file=ofile)
        print('-' * 60, file=ofile)
        apprvio(ionly, common.IONLY, ofile)
        apprvio(stack, common.STACK, ofile)
        apprvio(best, common.BEST, ofile)
    pass

if __name__ == '__main__':
    main()
