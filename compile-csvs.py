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
    import re
    import os
    base = os.path.basename(fname)

    bname = re.sub(r'_brt.*\.csv', '', base)

    return bname

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
        for line in ifile:
            csvs.append(line.strip())

    fields=None
    rows=[]
    for csvf in csvs:
        bname = fname2bname(csvf)
        with open(csvf, 'r') as ifile:
            reader = csv.DictReader(ifile)
            for row in reader:
                del row['']
                keys = row.keys()
                rows.append(row)
                fields=['bmark', *keys]
                row['bmark'] = bname

    logger.info(f'Writing single CSV file {parsed.outfile}')
    with open(parsed.outfile, 'w') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fields)
        writer.writeheader()
        [writer.writerow(row) for row in rows]

if __name__ == '__main__':
    main()
