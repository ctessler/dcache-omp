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

import re
import os

class CCArgs(argparse.ArgumentParser):
    '''Parses the command line arguments'''

    desc = '''
    Given a list of CSV file describing results from the run, compile them into
    a single CSV
    '''

    def __init__(self):
        super().__init__(
            description=self.desc,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        self.add_argument('filelist', nargs='?', help='Path to file list')
        self.add_argument('outfile', nargs='?', default='compiled.csv',
                          help='Name of the compiled output file '
                          'default:./compiled.csv')

def fname2bname(fname):
    '''Converts a filename to a benchmark name'''
    base = os.path.basename(fname)
    base = re.sub(fname2suite(fname) + '_', '', base)
    bname = re.sub(r'_brt.*\.csv', '', base)

    return bname

def fname2suite(fname):
    '''Converts a filename to a benchmark suite'''
    base = os.path.basename(fname)
    suite = re.sub(r'_.*', '', base)

    return suite

#
# Entry point
#
def main():
    argp = CCArgs()
    parsed = argp.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f'Reading CSV list from {parsed.filelist}')

    csvs = []
    with open(parsed.filelist, 'r') as ifile:
        [csvs.append(line.strip()) for line in ifile]

    fields=None
    rows=[]
    for csvf in csvs:
        bname = fname2bname(csvf)
        suite = fname2suite(csvf)
        with open(csvf, 'r') as ifile:
            reader = csv.DictReader(ifile)
            for row in reader:
                approach = row['method']
                if '' in row:
                    raise ValueError
                if 'Unnamed: 0' in row:
                    del row['Unnamed: 0']
                keys = row.keys()
                fields=['suite', 'appr', 'bmark', *keys]
                row['bmark'] = bname
                row['appr'] = approach
                row['suite'] = suite
                rows.append(row)

    logger.info(f'Writing single CSV file {parsed.outfile}')
    with open(parsed.outfile, 'w') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fields)
        writer.writeheader()
        [writer.writerow(row) for row in rows]

if __name__ == '__main__':
    main()
