import matplotlib

# Name of the approaches
IONLY='I-Only'
BEST=r'I&D-SFBest'
STACK=r'I&D-Stack'

# List of the approaches
appr = [ IONLY, STACK, BEST ]

# Formats an approach name for graphs
def appr2name(appr):
    '''Formats an approach name for graphs'''
    fmts={IONLY : 'I-Only',
          BEST  : r'I\&D-SFBest',
          STACK : r'I\&D-Stack'}

    return fmts[appr]

def appr2color(appr):
    colors={IONLY : 'black',
            BEST  : '#00008B',
            STACK : '#8C8C00'}

    colors={IONLY : 'C7',
            BEST  : 'C4',
            STACK : 'C1'}

    return colors[appr]

def appr2line(appr):
    lines={IONLY : ':',
           BEST  : '-',
           STACK : '-.'}

    lines={IONLY : '--',
           BEST  : '-',
           STACK : '-'}

    return lines[appr]

def appr2mark(appr):
    colors={IONLY : 'X',
            BEST  : 'v',
            STACK : 'o'}

    colors={IONLY : 'o',
            BEST  : '*',
            STACK : 's'}

    return colors[appr]


matplotlib.rcParams.update({
#    'font.family': 'Times',
    'font.family': 'serif',
    'font.size' : 16,
    'text.usetex': True,
#    'lines.linewidth' : 4.0,
    'lines.markersize' : 18.0,
#    'figure.figsize' : (11,8)
#    'text.latex.preamble' : r'''\usepackage{amsfonts}'''

})
