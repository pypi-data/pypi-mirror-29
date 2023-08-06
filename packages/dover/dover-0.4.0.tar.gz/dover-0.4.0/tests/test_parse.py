from itertools import product
import pytest
from dover import parse


version_strings = [''.join(p) for p in
                   product(('0.1', '0.1.0'), ('', '-'), ('d', 'dev'), ('', '.'), ('1',))]


@pytest.fixture(params=version_strings)
def ver_str(request):
    return request.param


def test_parse_version_number_rx_str(ver_str):
    rx = parse.get_raw_version_regex()
    m = rx.match(ver_str)
    assert m is not None
    assert m.groupdict()['version'] == ver_str


version_assignment_strings = [
    ('version = 0.2.3-dev.1', '0.2.3-dev.1'),
    ('__version__ = 0.2.3-dev.1',  '0.2.3-dev.1'),
    ('version: 0.2.3-dev.1', '0.2.3-dev.1')
]


@pytest.fixture(params=version_assignment_strings)
def ver_str_assign(request):
    return request.param


ver_assign_regex = parse.get_version_assignment_regex()


def test_find_version_assignment_regex(ver_str_assign):
    search_string, expected = ver_str_assign
    print(search_string)
    m = ver_assign_regex.match(search_string)
    assert m is not None
    assert m.groupdict()['version'] == expected


embedded_version_assignment_strings = [
    ('Welcome to Dummy v0.2.3-dev.1!', '0.2.3-dev.1'),
    ('[name](http://blah.foo.com/tags/v0.2.3-dev.1)',  '0.2.3-dev.1'),
    ('Dummy v0.2.3-dev.1 is the latest that needs', '0.2.3-dev.1')
]


@pytest.fixture(params=embedded_version_assignment_strings)
def ver_str_embedded(request):
    return request.param


ver_embedded_regex = parse.get_embedded_version_regex()


def test_find_embedded_version_regex(ver_str_embedded):
    search_string, expected = ver_str_embedded
    print(search_string)
    m = ver_embedded_regex.match(search_string)
    assert m is not None
    assert m.groupdict()['version'] == expected
