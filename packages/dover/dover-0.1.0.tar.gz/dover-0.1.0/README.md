## dover

##### A commandline utility for tracking and incrementing project version numbering.

### Usage

```bash
dover v0.1.0

dover is a commandline utility for incrementing code file version numbering.

Usage:
  dover [--list]
  dover increment (--major|--minor|--patch) [--apply]

Options:
  -M --major   Change major dover segment.
  -m --minor   Change minor dover segment.
  -p --patch   Change patch dover segment.
  -h --help    Show this help message
  --version    Show app dover.

```

### Basics

`dover` looks for either a specific **.dover** configuration file or
a **setup.cfg** file within the current directory.

Files that are to be tracked by `dover` should be listed in this format:

```ini
[dover:file:setup.py]
[dover:file:setup.cfg]
[dover:file:dover/cli.py]

```

### Current Project Version

Calling `dover` without any arguments returns the **current** version number
of the project.

```bash
... dover
0.1.0
...

```

### Currently Tracked File Status

Calling `dover` with the `--list` option, prints the project version and 
the list of all files and version strings being tracked:

```bash
... dover --list
Current Version: 0.1.0
Files:
    setup.py:005  `__version__ = '0.1.0'`
    setup.cfg:002  `version = 0.1.0`
    dover/cli.py:025  `__version__ = '0.1.0'`
...

```

### Reviewing Version Increment Changes

Calling `dover increment` with one the the segment options (e.g. `--minor`), will
print a listing of the propsed version change and the files that will be effected:

```bash
... dover increment --minor
Current Version: 0.1.0
New Version:     0.2.0
Files:
    setup.py  (0.1.0 -> 0.2.0)
    setup.cfg  (0.1.0 -> 0.2.0)
    dover/cli.py  (0.1.0 -> 0.2.0)
...
```

### Applying Version Increment Changes

To save the change make the same call with the `--apply` option:

```bash
... dover increment --minor --apply
Current Version: 0.1.0
New Version:     0.2.0
Files:
    setup.py  (0.1.0 -> 0.2.0)
    setup.cfg  (0.1.0 -> 0.2.0)
    dover/cli.py  (0.1.0 -> 0.2.0)
Version updates applied.
...
```

### What If There Is a Problem?

If at any point the versioning files being tracked are missaligned, `dover` will raise an error:

```bash
... dover increment --major --apply
Not all file versions match:

    setup.py:005  `__version__ = '0.1.0'`
    setup.cfg:002  `version = 0.3.0`
    dover/cli.py:025  `__version__ = '0.1.0'`
...
```
