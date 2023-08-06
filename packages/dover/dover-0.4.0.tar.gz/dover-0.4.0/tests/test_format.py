import pytest
from dover import format
from dover.version import Version


version_strings = (
    ('0.0.0r',    ('0', '0', '0',  '', 'r',  '',  ''), 'MmP!r!0'),
    ('000r',      ('0', '0', '0',  '', 'r',  '',  ''), 'MmP!r!0'),
    ('0.0r',      ('0', '0',  '',  '', 'r',  '',  ''), 'Mmp!r!0'),
    ('MmPr',      ('M', 'm', 'P',  '', 'r',  '',  ''), 'MmP!r!0'),
    ('Mmpr',      ('M', 'm', 'p',  '', 'r',  '',  ''), 'Mmp!r!0'),

    ('0.0.0-r.0', ('0', '0', '0', '-', 'r', '.', '0'), 'MmP-r.0'),
    ('000-r.0',   ('0', '0', '0', '-', 'r', '.', '0'), 'MmP-r.0'),
    ('0.0-r.0',   ('0', '0',  '', '-', 'r', '.', '0'), 'Mmp-r.0'),
    ('MmP-r.0',   ('M', 'm', 'P', '-', 'r', '.', '0'), 'MmP-r.0'),
    ('Mmp-r.0',   ('M', 'm', 'p', '-', 'r', '.', '0'), 'Mmp-r.0'),

    ('0.0.0r0',   ('0', '0', '0',  '', 'r',  '', '0'), 'MmP!r!0'),
    ('000r0',     ('0', '0', '0',  '', 'r',  '', '0'), 'MmP!r!0'),
    ('0.0r0',     ('0', '0',  '',  '', 'r',  '', '0'), 'Mmp!r!0'),
    ('MmPr0',     ('M', 'm', 'P',  '', 'r',  '', '0'), 'MmP!r!0'),
    ('Mmpr0',     ('M', 'm', 'p',  '', 'r',  '', '0'), 'Mmp!r!0'),

    ('0.0.0dev0', ('0', '0', '0',  '', 'dev',   '', '0'), 'MmP!R!0'),
    ('000alpha0', ('0', '0', '0',  '', 'alpha', '', '0'), 'MmP!R!0'),
    ('0.0beta0',  ('0', '0',  '',  '', 'beta',  '', '0'), 'Mmp!R!0'),
    ('MmPR0',     ('M', 'm', 'P',  '', 'R',     '', '0'), 'MmP!R!0'),

    ('1.1.1dev1', ('1', '1', '1',  '', 'dev',   '', '1'), 'MmP!R!0'),
    ('9.8.7dev6', ('9', '8', '7',  '', 'dev',   '', '6'), 'MmP!R!0'),
    ('3.3.3dev3', ('3', '3', '3',  '', 'dev',   '', '3'), 'MmP!R!0'),
    ('2.3.4dev5', ('2', '3', '4',  '', 'dev',   '', '5'), 'MmP!R!0'),
)


@pytest.fixture(params=version_strings)
def verstr(request):
    return request.param


VERSION_FMT_SEGMENTS = ('major', 'minor', 'patch', 'separator', 'prerel', 'dot', 'prversion')


def test_format_init(verstr):
    input, expected, normalized = verstr
    result = dict(zip(VERSION_FMT_SEGMENTS, expected))

    parsed_format = format.parse(input)
    normalized_format = format.normalize(parsed_format)

    assert parsed_format == result
    assert normalized_format == normalized


def test_format_error(capsys):
    with pytest.raises(format.VersionError):
        format.parse('012.Q.2')


def test_version_format():
    ver = Version('0.1.0')
    assert format.version_format(ver, 'MmP') == '0.1.0'
    assert format.version_format(ver, 'Mmp') == '0.1'

    ver = Version('0.1.1')
    assert format.version_format(ver, 'MmP') == '0.1.1'
    assert format.version_format(ver, 'Mmp') == '0.1.1'


prerelease_strings = (
    ('0.1.0',       '!r!0', ''),
    ('0.1.0-dev',   '!r!0', 'd'),
    ('0.1.0-dev.1', '!r!0', 'd1'),

    ('0.1.0',       '!R!0', ''),
    ('0.1.0-dev',   '!R!0', 'dev'),
    ('0.1.0-dev.1', '!R!0', 'dev1'),

    ('0.1.0',       '-R.0', ''),
    ('0.1.0-dev',   '-R.0', '-dev'),
    ('0.1.0-dev.1', '-R.0', '-dev.1'),
)


@pytest.fixture(params=prerelease_strings)
def prestr(request):
    return request.param


def test_prerelease_format(prestr):
    verstr, fmtstr, expected = prestr
    vers = Version(verstr)
    assert format.prerelease_format(vers.pre_release, fmtstr) == expected


version_format_strings = (
    ('0.1.0',       'MmP!r!0', '0.1.0'),
    ('0.1.0-dev',   'MmP!r!0', '0.1.0d'),
    ('0.1.0-dev.1', 'MmP!r!0', '0.1.0d1'),

    ('0.1.0',       'MmP!R!0', '0.1.0'),  # 4
    ('0.1.0-dev',   'MmP!R!0', '0.1.0dev'),
    ('0.1.0-dev.1', 'MmP!R!0', '0.1.0dev1'),

    ('0.1.0',       'MmP-R.0', '0.1.0'),
    ('0.1.0-dev',   'MmP-R.0', '0.1.0-dev'),
    ('0.1.0-dev.1', 'MmP-R.0', '0.1.0-dev.1'),

    ('0.1.0',       '000r', '0.1.0'),  # 10
    ('0.1.0-dev',   '000r', '0.1.0d'),
    ('0.1.0-dev.1', '000r', '0.1.0d1'),

    ('0.1.0',       '000R', '0.1.0'),
    ('0.1.0-dev',   '000R', '0.1.0dev'),
    ('0.1.0-dev.1', '000R', '0.1.0dev1'),

    ('0.1.0',       '000R', '0.1.0'),  # 16
    ('0.1.0-dev',   '000R', '0.1.0dev'),
    ('0.1.0-dev.1', '000R', '0.1.0dev1'),

    ('0.1.0',       '00r', '0.1'),  # 19
    ('0.1.0-dev',   '00r', '0.1d'),
    ('0.1.0-dev.1', '00r', '0.1d1'),
)


@pytest.fixture(params=version_format_strings)
def full_ver_str(request):
    return request.param


def test_full_version_format(full_ver_str):
    verstr, fmtstr, expected = full_ver_str
    assert format.format_version(fmtstr, Version(verstr)) == expected
