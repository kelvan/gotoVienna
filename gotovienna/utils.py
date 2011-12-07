# -*- coding: utf-8 -*-

def inred(x):
    return '\033[91m' + x + '\033[0m'

def ingreen(x):
    return '\033[92m' + x + '\033[0m'

def inblue(x):
    return '\033[94m' + x + '\033[0m'

def sort_departures(dep):
    print 'sorting ...'
    d = sorted(dep, lambda x, y: cmp(x['atime'], y['atime']))
    print map(lambda x: x['atime'], d)
    return d
