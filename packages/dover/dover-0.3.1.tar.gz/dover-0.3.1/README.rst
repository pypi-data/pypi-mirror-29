dover v0.3.1
============

.. image:: https://img.shields.io/badge/version-v0.3.1-green.svg
.. image:: https://img.shields.io/badge/coverage-100%25-green.svg

A commandline utility for incrementing your project version numbers.


Installation
^^^^^^^^^^^^

.. code-block:: text
    
    ... pip install dover


What does it do?
^^^^^^^^^^^^^^^^

When ``dover`` is run from the root directory of your project, it does the 
following:

    1. looks for a configuration file (``.dover``, ``.dover.ini``, ``setup.cfg``)
    2. reads any ``dover`` configuration line in this format:

       .. code-block:: text
            
           [dover:file:relatvie/file.pth]

    3. searches the configured file references for "version" strings
    4. validates all version strings across all configured files.
    5. displays and/or increments the version strings based upon 
       cli options. 

Usage
^^^^^

.. code-block:: text 
    
    ... dover --help

    dover v0.3.1

    dover is a commandline utility for 
    tracking and incrementing your 
    project version numbers.

    Usage:
      dover           [--list] [--debug]
      dover increment ((--major|--minor|--patch) [--alpha|--beta|--rc] |
                       [--major|--minor|--patch] (--alpha|--beta|--rc)) 
                       [--apply] [--debug] [--no-list]

    Options:
      -M --major   Update major version segment.
      -m --minor   Update minor version segment.
      -p --patch   Update patch version segment.
      -a --alpha   Update alpha pre-release segment.
      -b --beta    Update beta pre-release segment.
      -r --rc      Update release candidate segment.
      --debug      Print full exception info.
      -h --help    Display this help message
      --version    Display dover version.



See `Read  The Docs <http://dover.readthedocs.io/en/latest/>`_ for more.
