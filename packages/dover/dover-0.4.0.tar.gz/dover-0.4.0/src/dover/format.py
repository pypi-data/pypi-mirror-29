import re
from .util import VersionError


FORMAT_RX = re.compile(
    (r'^(?P<major>(\d|M))\.?(?P<minor>(\d|m))(\.(?=[p|P|\d]))?(?P<patch>(p|P|\d)?)'
     r'(?P<separator>[\.\!-]?)'
     r'(?P<prerel>(R|r|d|a|b|rc|D|A|B|dev|alpha|beta))'
     r'(?P<dot>[\.\!-]?)'
     r'(?P<prversion>\d?)'
     r'$'))


VERSION_FMT_SEGMENTS = {
    'major': (('0123456789M', 'M'),),
    'minor': (('0123456789m', 'm'),),
    'patch': ((('P', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'), 'P'), (('', 'p'), 'p')),
    'separator': (('', '!'),),
    'prerel': ((('R', 'D', 'A', 'B', 'dev', 'alpha', 'beta'), 'R'),
               ('rdab', 'r')),
    'dot': (('', '!'),),
    'prversion': ((('', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'), '0'),),
}


def parse(format_string):
    match = FORMAT_RX.match(format_string)
    if not match:
        raise VersionError('`{}` is not a valid format string.'.format(format_string))
    return match.groupdict()


def normalize(parsed_formats):
    _normalized = {}
    for key, value in VERSION_FMT_SEGMENTS.items():
        input_fmt = parsed_formats[key]
        for code_matches, normalized_code in value:
            if input_fmt in code_matches:
                _normalized[key] = normalized_code
                break
            _normalized[key] = input_fmt

    return '{major}{minor}{patch}{separator}{prerel}{dot}{prversion}'.format(**_normalized)


def version_format(vers, fmt):
    fmt_str = '{0.major}.{0.minor}'.format(vers)
    if fmt[2] == 'p' and vers.patch == 0:
        return fmt_str
    return '{}.{}'.format(fmt_str, vers.patch)


def prerelease_format(prerel, fmt):
    sep = '' if fmt[0] == '!' else fmt[0]
    pre = prerel.state.__format__(fmt[1])

    if not pre:
        return ''

    if prerel.number == 0:
        return ''.join((sep, pre))

    dot = '' if fmt[2] == '!' else fmt[2]
    num = str(prerel.number)
    return ''.join((sep, pre, dot, num))


def format_version(fmt, vers):
    if not fmt:
        return str(vers)
    parsed_format = parse(fmt)
    normalized_format = normalize(parsed_format)
    version_fmt = version_format(vers, normalized_format[:3])
    prerelease_fmt = prerelease_format(vers.pre_release, normalized_format[3:])
    return version_fmt + prerelease_fmt


def format_factory(fmt_str):
    _fmt = '{{:{}}}'

    if fmt_str:
        _fmt = _fmt.format(fmt_str)
    else:
        _fmt = _fmt.format('')

    def _formatter(ver_obj):
        return _fmt.format(ver_obj)

    return _formatter
