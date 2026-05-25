# Name of the approaches
IONLY='I-Only'
SFDBEST=r'I&D-SFBest'
STACK=r'I&D-Stack'

# List of the approaches
appr = [ IONLY, STACK, SFDBEST ]

# Formats an approach name for graphs
def appr2name(appr):
    '''Formats an approach name for graphs'''
    fmts={IONLY   : 'I-Only',
          SFDBEST : r'I&D-SFBest',
          STACK   : r'I&D-Stack'}

    return fmts[appr]

def appr2color(appr):
    colors={IONLY   : 'black',
            SFDBEST : '#00008B',
            STACK   : '#8C8C00'}

    return colors[appr]

def appr2line(appr):
    colors={IONLY   : ':',
            SFDBEST : '-',
            STACK   : '-.'}

    return colors[appr]
