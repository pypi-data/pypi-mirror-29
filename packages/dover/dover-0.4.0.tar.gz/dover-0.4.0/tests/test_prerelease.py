import pytest
from dover.version import PRState, PreRelease, VersionError


def test_prstate_access():
    assert PRState.null == 0
    assert PRState['null'] == PRState.null
    assert PRState[str(PRState.alpha)] == PRState.alpha


def test_prstate_str():
    assert str(PRState.null) == ''
    assert str(PRState.dev) == 'dev'
    assert str(PRState.alpha) == 'alpha'
    assert str(PRState.beta) == 'beta'
    assert str(PRState.rc) == 'rc'


def test_prstate_basic_format():
    assert '{:R}'.format(PRState.null) == ''
    assert '{:r}'.format(PRState.null) == ''
    assert '{:R}'.format(PRState.dev) == 'dev'
    assert '{:r}'.format(PRState.dev) == 'd'
    assert '{:R}'.format(PRState.alpha) == 'alpha'
    assert '{:r}'.format(PRState.alpha) == 'a'
    assert '{:R}'.format(PRState.beta) == 'beta'
    assert '{:r}'.format(PRState.beta) == 'b'
    assert '{:R}'.format(PRState.rc) == 'rc'
    assert '{:r}'.format(PRState.rc) == 'rc'


def test_prstate_contains():
    assert PRState.contains('dev')
    assert PRState.contains('null')
    assert PRState.contains('alpha')
    assert PRState.contains('beta')
    assert PRState.contains('rc')
    assert PRState.contains('release')

    assert not PRState.contains('')


def test_prerelease_init():
    pre = PreRelease()
    assert not pre.exists
    pre.initialize('alpha', 0)
    assert pre.exists


def test_prerelease_str():
    pre = PreRelease()
    assert str(pre) == ''
    pre.initialize('alpha', 0)
    assert str(pre) == '-alpha'
    pre.increment_number()
    assert str(pre) == '-alpha.1'


def test_prerelease_to_tuple():
    variations = [
        (('null',  0), (0, 0)),
        (('dev',   0), (1, 0)),
        (('dev',   1), (1, 1)),
        (('alpha', 0), (2, 0)),
        (('alpha', 1), (2, 1)),
        (('alpha', 0), (2, 0)),
        (('beta',  0), (3, 0)),
        (('beta',  1), (3, 1)),
        (('beta',  1), (3, 1)),
        (('rc',    0), (4, 0)),
        (('rc',    1), (4, 1)),
        (('rc',    2), (4, 2)),
    ]
    pre = PreRelease()
    for initialize, expected_results in variations:
        print(initialize, expected_results)
        pre.initialize(*initialize)
        assert pre.to_tuple() == expected_results


def test_prerelease_increment():
    variations = [
        (('null', 0), 'alpha', '-alpha'),
        (('alpha', 0), 'alpha', '-alpha.1'),
        (('alpha', 1), 'alpha', '-alpha.2'),
        (('alpha', 0), 'beta', '-beta'),
        (('beta', 0), 'beta', '-beta.1'),
        (('beta', 1), 'beta', '-beta.2'),
        (('beta', 1), 'rc', '-rc'),
        (('rc', 0), 'rc', '-rc.1'),
        (('rc', 1), 'rc', '-rc.2'),
        (('rc', 2), 'null', '')
    ]
    pre = PreRelease()
    for initialize, increment, expected_results in variations:
        print(initialize, increment, expected_results)
        pre.initialize(*initialize)
        pre.increment(increment)
        assert str(pre) == expected_results


def test_prerelease_increment_errors():
    pre = PreRelease()

    pre.initialize('rc', 0)

    with pytest.raises(VersionError):
        pre.increment('alpha')

    with pytest.raises(VersionError):
        pre.increment('beta')

    pre.initialize('beta', 0)

    with pytest.raises(VersionError):
        pre.increment('alpha')

    with pytest.raises(VersionError):
        pre.increment('dev')

    with pytest.raises(VersionError):
        pre.increment('something')
