from enum import IntEnum
from . import format as formatter
from . import parse
from .util import VersionError


class PRState(IntEnum):

    release = -1

    null = 0

    dev = 1
    alpha = 2
    beta = 3
    rc = 4

    # aliases
    d = 1
    a = 2
    b = 3

    @classmethod
    def contains(cls, name):
        if isinstance(name, str):
            return name in cls.__members__
        return name in cls

    @classmethod
    def get(cls, name):
        if not name:
            name = 'null'
        return cls[str(name)]

    def __str__(self):
        if self in (PRState.null, PRState.release):
            return ''
        return self.name

    def __format__(self, fmt):
        if fmt == 'r' and self in (1, 2, 3):
            return str(self.name)[0]
        return str(self)


class PreRelease(object):

    def __init__(self):
        self.state = PRState.null
        self.number = 0

    def initialize(self, state=PRState.null, number=0):
        self.state = PRState.get(state)
        self.number = number

    def reset(self):
        self.initialize()

    @property
    def exists(self):
        return self.state is not PRState.null

    def increment(self, state):

        if not PRState.contains(state):
            raise VersionError('Unrecognized pre-release name: `{}`.'.format(state))

        state = PRState.get(state)

        if state in (PRState.null, PRState.release):
            self.reset()
        elif self.state in (PRState.null, PRState.release):
            # this will set the pre-relase to
            # whatever the state is and skip the natural sequence
            self.state = state
            self.number = 0
        elif state == self.state:
            self.increment_number()
        elif state > self.state:
            self.initialize(state, 0)
        else:
            err_msg = ('Invalid pre-release sequence requested: '
                       '`{}` release preceeds `{}`.')
            raise VersionError(err_msg.format(state, self.state))

    def increment_number(self):
        self.number += 1

    def to_tuple(self):
        return (self.state.value, self.number)

    def __str__(self):
        if not self.exists:
            return ''
        if self.number == 0:
            number_str = ''
        else:
            number_str = '.{}'.format(self.number)
        return '-{}{}'.format(self.state, number_str)


class Version(object):

    MAJOR = 'major'
    MINOR = 'minor'
    PATCH = 'patch'
    DEV = 'dev'
    ALPHA = 'alpha'
    BETA = 'beta'
    RC = 'rc'

    _names = (None, 'major', 'minor', 'patch')

    _vers_regex = parse.get_raw_version_regex()

    def __init__(self, version_string='0.1.0'):
        vmatch = self._vers_regex.match(version_string)
        if not vmatch:
            msg = '"{}" is an invalid version string.'
            raise VersionError(msg.format(version_string))

        vstr = vmatch.groupdict()

        self.major = int(0 if not vstr['major'] else vstr['major'])
        self.minor = int(0 if not vstr['minor'] else vstr['minor'])
        self.patch = int(0 if not vstr['patch'] else vstr['patch'])
        # pre-release
        self.pre_release = PreRelease()
        _pre_name = None if not vstr['pre_release'] else vstr['pre_release']
        _pre_number = int(0 if not vstr['pre_number'] else vstr['pre_number'])
        self.pre_release.initialize(_pre_name, _pre_number)

    def copy(self):
        return Version(str(self))

    def increment(self, part, pre_release=PRState.null):
        if part not in self._names:
            raise VersionError('`{}` is not a valid version part.'.format(part))

        if not part and pre_release is PRState.null:
            raise VersionError('No version section has been selected.')

        self.increment_part(part)

        if pre_release in (PRState.null, PRState.release) or (part and pre_release):
            self.pre_release.reset()

        if pre_release not in (PRState.null, PRState.release):
            self.pre_release.increment(pre_release)

    def increment_part(self, part):
        if part == 'major':
            self.increment_major()
        elif part == 'minor':
            self.increment_minor()
        elif part == 'patch':
            self.increment_patch()

    def increment_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0

    def increment_minor(self):
        self.minor += 1
        self.patch = 0

    def increment_patch(self):
        self.patch += 1

    def to_tuple(self):
        if self.pre_release.exists:
            return (self.major, self.minor, self.patch, self.pre_release)
        return (self.major, self.minor, self.patch)

    def __eq__(self, obj):
        return str(self) == str(obj)

    def __str__(self):
        version = self.to_tuple()
        ver_str = '.'.join([str(i) for i in version[:3]])
        if len(version) > 3:
            ver_str += str(version[3])
        return ver_str

    def __repr__(self):
        return '<Version {0}>'.format(self)

    def __format__(self, fmt):
        return formatter.format_version(fmt, self)
