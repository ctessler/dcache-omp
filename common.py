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

    return colors[appr]

def appr2line(appr):
    colors={IONLY : ':',
            BEST  : '-',
            STACK : '-.'}

    return colors[appr]

def appr2mark(appr):
    colors={IONLY : 'X',
            BEST  : 'v',
            STACK : 'o'}

    return colors[appr]


matplotlib.rcParams.update({
    'font.family': 'Times',
    'font.size' : int(14),
    'text.usetex': True,
    'text.latex.preamble' : r'''\usepackage{amsfonts}'''
})
