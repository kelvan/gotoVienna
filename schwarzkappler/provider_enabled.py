import sys
import os

sys.path.insert(0, os.path.abspath(__file__))
from provider import vienna_at, schwarzkappler

enabled_provider = [vienna_at.ViennaAt, schwarzkappler.Schwarzkappler]

def _filter_by_line(warnings, line):
    if warnings.has_key(line):
        return warnings[line]
    else:
        return []

def get_all_warnings(line=None):
    """ fetch all schwarzkappler warnings from enabled provider, filter by line optional
    """
    
    if line:
        warnings = []
    else:
        warnings = {}
    for provider in enabled_provider:
        if provider.need_update:
            provider.fetch()
        
        info = provider.info
        
        if line:
            warnings += _filter_by_line(info, line)
        else:
            for key in info.keys():
                if warnings.has_key(key):
                    warnings[key] += info[key]
                else:
                    warnings[key] = info[key]

    return warnings
