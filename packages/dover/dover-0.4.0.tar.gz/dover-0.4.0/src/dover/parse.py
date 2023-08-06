import re


# Common version regex string
VERSION_NUMBER_RX_STR = (r'(?P<version>'
                         r'(?P<major>\d+)'
                         r'(\.(?P<minor>\d+))?'
                         r'(\.(?P<patch>\d+))?'
                         r'([-\.]?(?P<pre_release>(dev|alpha|beta|rc|d|a|b))'
                         r'(\.?(?P<pre_number>\d+))?)?'
                         r')')


def get_raw_version_regex():
    return re.compile(r'^' + VERSION_NUMBER_RX_STR + r'$', re.I)


def get_version_assignment_regex():
    '''Match version assignment strings - what we would
    find in code or configuration files.

    '''
    return re.compile((r'''^((__version__|version) ?[=:]? ?v?)'''
                       r'''['"]?''' + VERSION_NUMBER_RX_STR +
                       r'''['"]?$'''), re.I)


def get_embedded_version_regex():
    '''Match embedded version strings - what we would expect
    to find in documentation.

    '''
    return re.compile(r'''^.*[ \/\-"']v''' + VERSION_NUMBER_RX_STR + r'''[ \-"']?.*$''', re.I)
