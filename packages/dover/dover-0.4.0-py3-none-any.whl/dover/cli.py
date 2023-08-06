# -*- coding: utf-8 -*-
'''
dover v0.4.0

dover is a commandline utility for
tracking and incrementing your
project version numbers.

Usage:
  dover [--list] [--debug] [--format=<fmt>]
  dover increment ((--major|--minor|--patch)
                   [--dev|--alpha|--beta|--rc] |
                   [--major|--minor|--patch]
                   (--dev|--alpha|--beta|--rc) | --release)
                   [--apply] [--debug] [--no-list] [--format=<fmt>]

Options:
  -M --major      Update major version segment.
  -m --minor      Update minor version segment.
  -p --patch      Update patch version segment.
  -d --dev        Update dev version segment.
  -a --alpha      Update alpha pre-release segment.
  -b --beta       Update beta pre-release segment.
  -r --rc         Update release candidate segment.
  -R --release    Clear pre-release version.
  -x --no-list    Do not list files.
  --format=<fmt>  Apply format string.
  --debug         Print full exception info.
  -h --help       Display this help message
  --version       Display dover version.

'''
from docopt import docopt
from . import commands


__author__ = 'Mark Gemmill'
__email__ = 'dev@markgemmill.com'
__version__ = '0.4.0'


def main():
    cargs = docopt(__doc__, version='dover v{}'.format(__version__))

    if cargs['increment']:
        commands.increment(cargs)  # pylint: disable=no-value-for-parameter

    elif cargs['--list']:
        commands.display(cargs)  # pylint: disable=no-value-for-parameter

    else:
        commands.version(cargs)
