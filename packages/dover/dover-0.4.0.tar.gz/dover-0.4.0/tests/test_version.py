import pytest
from dover.version import Version, VersionError


def test_init():
    version = Version('0.0.1')
    assert version.major == 0
    assert version.minor == 0
    assert version.patch == 1


def test_version_init_errors():
    with pytest.raises(VersionError):
        Version('v0.1.2alpha')


def test_version_copy():
    ver1 = Version('2.3.6-rc.1')
    ver2 = ver1.copy()
    assert ver1 == ver2


def init_variation(initializer, expected):
    version = Version(initializer)
    assert str(version) == expected


def test_init_variations():
    variations = [
        ('0', '0.0.0'),
        ('0.0', '0.0.0'),
        ('0.0.0', '0.0.0'),
        ('2', '2.0.0'),
        ('2.0', '2.0.0'),
        ('2.0.0', '2.0.0'),
        ('0.1', '0.1.0'),
        ('0.1.0', '0.1.0'),
        ('0.1.1', '0.1.1'),
        ('0.1.1-alpha', '0.1.1-alpha')
    ]

    for initializer, expected in variations:
        init_variation(initializer, expected)


def test_formating():
    version = Version('0.1.0')
    assert '{}'.format(version) == '0.1.0'
    assert '{:00r}'.format(version) == '0.1'
    assert '{:000r}'.format(version) == '0.1.0'

    version = Version('0.1.0d3')
    assert '{}'.format(version) == '0.1.0-dev.3'
    assert '{:00r}'.format(version) == '0.1d3'
    assert '{:000r}'.format(version) == '0.1.0d3'
    assert '{:000.R.}'.format(version) == '0.1.0.dev.3'


def test_str():
    version = Version('0.0.1')
    assert str(version) == '0.0.1'


def test_to_string():
    version = Version('0.0.1')
    assert str(version) == '0.0.1'


def test_to_tuple():
    version = Version('0.0.1')
    assert version.to_tuple() == (0, 0, 1)


def test_repr():
    version = Version('0.0.1')
    assert repr(version) == '<Version 0.0.1>'


def test_increment_major():
    version = Version('1.1.1')
    version.increment_major()
    assert str(version) == '2.0.0'


def test_increment_minor():
    version = Version('1.1.1')
    version.increment_minor()
    assert str(version) == '1.2.0'


def test_increment_patch():
    version = Version('1.1.1')
    version.increment_patch()
    assert str(version) == '1.1.2'


def test_increment():
    version = Version('0.1.0')

    version.increment('patch')
    assert str(version) == '0.1.1'

    version.increment('patch', 'alpha')
    assert str(version) == '0.1.2-alpha'

    version.increment('patch', 'alpha')
    assert str(version) == '0.1.3-alpha'

    version.increment('minor')
    assert str(version) == '0.2.0'

    version.increment(None, 'beta')
    assert str(version) == '0.2.0-beta'

    version.increment(None, 'beta')
    assert str(version) == '0.2.0-beta.1'

    version.increment(None, 'beta')
    assert str(version) == '0.2.0-beta.2'

    version.increment(None, 'rc')
    assert str(version) == '0.2.0-rc'

    version.increment(None, 'rc')
    assert str(version) == '0.2.0-rc.1'

    version.increment('major')
    assert str(version) == '1.0.0'


def test_increment_errors():
    version = Version('0.1.0')
    with pytest.raises(VersionError):
        version.increment('alpha')

    with pytest.raises(VersionError):
        version.increment(None)
