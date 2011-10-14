#!/usr/bin/env python

from distutils.core import setup

import re
import glob

PACKAGE = 'gotovienna'
SCRIPT_FILE = 'gotovienna-qml'

main_py = open(SCRIPT_FILE).read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", main_py))
docstrings = re.findall('"""(.*?)"""', main_py, re.DOTALL)

# List the modules that need to be installed/packaged
PACKAGES = (
        PACKAGE,
)

# Metadata fields extracted from SCRIPT_FILE
AUTHOR_EMAIL = metadata['author']
VERSION = metadata['version']
WEBSITE = metadata['website']
LICENSE = metadata['license']
DESCRIPTION = docstrings[0].strip()
if '\n\n' in DESCRIPTION:
    DESCRIPTION, LONG_DESCRIPTION = DESCRIPTION.split('\n\n', 1)
else:
    LONG_DESCRIPTION = None

# Extract name and e-mail ("Firstname Lastname <mail@example.org>")
AUTHOR, EMAIL = re.match(r'(.*) <(.*)>', AUTHOR_EMAIL).groups()

DATA_FILES = [
        ('share/gotovienna', ['images/gotovienna_qml80.png']),
        ('share/gotovienna/qml', glob.glob('qml/*')),
]

setup(name=PACKAGE,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=EMAIL,
      license=LICENSE,
      url=WEBSITE,
      packages=PACKAGES,
      scripts=[SCRIPT_FILE],
      data_files=DATA_FILES,
      download_url=WEBSITE+PACKAGE+'-'+VERSION+'.tar.gz')

