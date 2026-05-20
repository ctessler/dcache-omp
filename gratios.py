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
        self.add_argument('pfx', nargs='?', default='gratio-',
                          help='Name of the output file prefix '
                          'default:./gratio-')
        self.add_argument('ext', nargs='?', default='pdf',
                          help='Type of the output file '
                          'default:./pdf')


def byfield(df, field, xlabel):
    gkeys = [field]
    groups = df.groupby(gkeys, group_keys=True)
    graphf = groups[['tmratio', 'dmratio', 'imratio']].mean()

    fig, ax = plt.subplots()
    ax.plot(graphf.index, graphf['tmratio'], marker='x', label='Cache Miss Ratio')
    ax.plot(graphf.index, graphf['dmratio'], marker='o', label='Data Cache Miss Ratio')
    ax.plot(graphf.index, graphf['imratio'], marker='.', label='Instruction Cache Miss Ratio')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Ratio')

    ax.set_xscale('symlog', base=2)
    ax.set_xticks(graphf.index)
    ax.legend()

    import matplotlib.ticker
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())

    return fig

def bysets(parsed, df):
    fig = byfield(df, 'cache_sets', 'Cache Sets')

    fname = parsed.pfx + 'sets.' + parsed.ext
    fig.savefig(fname)
    fig.clear()

def byblocks(parsed, df):
    fig = byfield(df, 'blk_size', 'Block Size (Bytes)')

    fname = parsed.pfx + 'blocks.' + parsed.ext
    fig.savefig(fname)
    fig.clear()

def byassoc(parsed, df):
    fig = byfield(df, 'assoc', 'Associativity)')
    fname = parsed.pfx + 'assoc.' + parsed.ext
    fig.savefig(fname)
    fig.clear()

def bythreads(parsed, df):
    fig = byfield(df, 'threads', 'Threads')

    fname = parsed.pfx + 'threads.' + parsed.ext
    fig.savefig(fname)
    fig.clear()

def byfieldbar(df, field, xlabel):
    gkeys = [field]
    groups = df.groupby(gkeys, group_keys=True)
    graphf = groups[['tmratio', 'dmratio', 'imratio']].mean()

    bargroups = len(graphf.index)
    barpos = np.arange(bargroups)
    barwidth = .3

    fig, ax = plt.subplots()
    ax.bar(barpos + (0 * barwidth), graphf['tmratio'], barwidth, label='Cache Miss Ratio')
    ax.bar(barpos + (1 * barwidth), graphf['dmratio'], barwidth, label='Data Cache Miss Ratio')
    ax.bar(barpos + (2 * barwidth), graphf['imratio'], barwidth, label='Instruction Cache Miss Ratio')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Ratio')

    ax.set_xticks(barpos + barwidth, graphf.index)
    ax.legend()

    return fig

def barsets(parsed, df):
    fig = byfieldbar(df, 'cache_sets', 'Cache Sets')
    fname = parsed.pfx + 'sets-bar.' + parsed.ext
    fig.savefig(fname)
    fig.clear()

def barassoc(parsed, df):
    fig = byfieldbar(df, 'assoc', 'Associativity')
    fname = parsed.pfx + 'assoc-bar.' + parsed.ext
    fig.savefig(fname)
    fig.clear()

def barthreads(parsed, df):
    fig = byfieldbar(df, 'threads', 'Threads')
    fname = parsed.pfx + 'threads-bar.' + parsed.ext
    fig.savefig(fname)
    fig.clear()

def barblocks(parsed, df):
    fig = byfieldbar(df, 'blk_size', 'Block Size (bytes)')
    fname = parsed.pfx + 'bocks-bar.' + parsed.ext
    fig.savefig(fname)
    fig.clear()



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

    bysets(parsed, df)
    byblocks(parsed, df)
    byassoc(parsed, df)
    bythreads(parsed, df)

    barsets(parsed, df)
    barblocks(parsed, df)
    barassoc(parsed, df)
    barthreads(parsed, df)



if __name__ == '__main__':
    main()
