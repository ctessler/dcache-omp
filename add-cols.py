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

IONLY='base'

# Argument parsing
import argparse
import csv
import logging

import pandas as pd

class AWArgs(argparse.ArgumentParser):
    '''Parses the command line arguments'''

    desc = '''
    Given a list of CSV file describing results from the run, compile them into
    a single CSV
    '''

    def __init__(self):
        super().__init__(
            description=self.desc,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        self.add_argument('icsv', nargs='?',
                          help='Path to file csv from compiled-cvs.py')
        self.add_argument('ocsv', nargs='?', default='obs.csv',
                          help='Name of the output file with run-time'
                          'default:./obs.csv')

#
# Entry point
#
def main():
    argp = AWArgs()
    parsed = argp.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f'Reading CSV file {parsed.icsv}')
    df = pd.read_csv(parsed.icsv)

    # Hit and miss ratios
    df['dmratio'] = df['dmiss'] / (df['dmiss'] + df['dhit'])
    df['dhratio'] = df['dhit']  / (df['dmiss'] + df['dhit'])
    df['imratio'] = df['imiss'] / (df['imiss'] + df['ihit'])
    df['ihratio'] = df['ihit']  / (df['imiss'] + df['ihit'])
    df['tmratio'] = (df['dmiss'] + df['imiss']) / (df['dmiss'] + df['dhit'] + df['imiss'] + df['ihit'])
    df['thratio'] = (df['dhit'] + df['dhit']) / (df['dmiss'] + df['dhit'] + df['imiss'] + df['ihit'])

    # Observed execution times
    df['obs'] = df['dmiss'] * df['brt'] + df['dhit'] + df['imiss'] * df['brt'] + df['ihit']

    # Add the comparisons to the ionly approach
    basef = df[df['appr'] == IONLY].copy()
    drops = basef.filter(regex='appr', axis=1).columns
    basef = basef.drop(columns=drops)
    mergecols = ['bmark', 'threads', 'brt', 'assoc', 'blk_size',
                 'cache_sets']

    combf = pd.merge(df, basef, suffixes=['','_ionly'], how='inner',
                     on=mergecols)
    for metric in ['dmiss', 'dhit', 'imiss', 'ihit', 'obs',
                   'dmratio', 'dhratio', 'imratio', 'ihratio',
                   'tmratio', 'thratio']:
        ionly = metric + '_ionly'
        dif = metric + '_iodif'
        pct = metric + '_iopct'
        combf[dif] = combf[ionly] - combf[metric]
        combf[pct] = 100 * (combf[metric] / combf[ionly])
        combf[pct] = combf[pct].round(2)

    logger.info(f'Writing CSV file {parsed.ocsv}')
    combf.to_csv(parsed.ocsv, index=False)

if __name__ == '__main__':
    main()
