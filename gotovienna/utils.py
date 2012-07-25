# -*- coding: utf-8 -*-

def inred(x):
    return '\033[91m' + x + '\033[0m'

def ingreen(x):
    return '\033[92m' + x + '\033[0m'

def inblue(x):
    return '\033[94m' + x + '\033[0m'

def sort_departures(dep):
    #print 'sorting ...'
    d = sorted(dep, lambda x, y: cmp(x['departure'], y['departure']))
    #print map(lambda x: x['departure'], d)
    return d

def clean_text(text):
    return text.replace('&nbsp;', ' ').strip()
