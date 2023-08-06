dover v0.4.0
============

.. image:: https://img.shields.io/badge/version-v0.4.0-green.svg
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



See `Read  The Docs <http://dover.readthedocs.io/en/latest/>`_ for more.


History
^^^^^^^

0.4.0 (2018-03-10
-----------------

- Added `--dev` option as a pre-release state.
- Added `--release` option that clears any pre-release
  versioning.
- Added `--format` option that allows user to control the
  format from the standard `0.0.0-dev.1` format.


0.3.1 (2018-03-02)
------------------

- documentation update to deal with 
  invalid README formating.


0.3.0 (2018-03-02)
------------------

- added pre-release options
- added --no-list option
- expanded documentation
- 100% code coverage


0.2.1 (2018-02-22)
------------------

-  expanded tests
-  general code clean up


0.2.0 (2018-02-22)
------------------

-  improved alignment of output
-  added additional version matching check


0.1.0 (2018-02-18)
------------------

-  initial commit


