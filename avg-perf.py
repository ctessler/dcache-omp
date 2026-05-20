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

import pandas as pd

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
        self.add_argument('ocsv', nargs='?', default='ratios.csv',
                          help='Name of the output file '
                          'default:./ratios.csv')

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

    # (data,instruction,total) cache miss and and hit ratios
    df['dmratio'] = df['dmiss'] / (df['dmiss'] + df['dhit'])
    df['dhratio'] = df['dhit']  / (df['dmiss'] + df['dhit'])
    df['imratio'] = df['imiss'] / (df['imiss'] + df['ihit'])
    df['ihratio'] = df['ihit']  / (df['imiss'] + df['ihit'])
    df['tmratio'] = (df['dmiss'] + df['imiss']) / (df['dmiss'] + df['dhit'] + df['imiss'] + df['ihit'])
    df['thratio'] = (df['dhit'] + df['dhit']) / (df['dmiss'] + df['dhit'] + df['imiss'] + df['ihit'])

    df = df.round({'dmratio': 3, 'dhratio':3,
              'imratio': 3, 'ihratio':3})

    logger.info(f'Writing CSV file {parsed.ocsv}')
    df.to_csv(parsed.ocsv, index=False)

    print("Averages:")
    for key in ['dmratio', 'dhratio',
                'imratio', 'ihratio',
                'tmratio', 'thratio']:
        print(f'{key} {df[key].mean():.2f}')

if __name__ == '__main__':
    main()
