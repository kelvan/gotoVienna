from urllib2 import urlopen
from hashlib import md5
from datetime import datetime
import os
from os import path
from config import config

CONFIGDIR = path.expanduser('~/.gotovienna')
STATIONFILENAME = path.join(CONFIGDIR, 'stations.db')
URLPREFIX = 'http://www.logic.at/people/kelvan/python/gotovienna/downloads/%s'
REMOTEFILE = 'stations.db'
REMOTEHASH = 'stations.md5'

def compare_hash(md5sum, fn):
    localmd5 = md5()
    md5sum = md5sum.split()[0]

    if not path.exists(fn):
        # File doesn't exist
        return False

    with open(fn,'rb') as f: 
        for chunk in iter(lambda: f.read(8192), ''): 
             localmd5.update(chunk)
    return localmd5.hexdigest() == md5sum

def check_stations_update():
    """ Check for new version of stations.db
        return True if new version available
        return False if not
        raise exception if unable to check for new version
    """
    remote_hash = urlopen(URLPREFIX % REMOTEHASH).read()
    return not compare_hash(remote_hash, STATIONFILENAME)

def update_stations():
    if not path.exists(CONFIGDIR):
        os.mkdir(CONFIGDIR)
    remote = urlopen(URLPREFIX % REMOTEFILE)
    with open(STATIONFILENAME, 'wb') as f:
        f.write(remote.read())
    config.setLastStationsUpdate(datetime.now().strftime('%c'))
    return True
