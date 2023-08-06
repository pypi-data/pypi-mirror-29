import sys
from functools import wraps
from .version import Version, PRState
from .format import format_factory
from . import project


def command(func):

    @wraps(func)
    def _command(cargs, *args, **kwargs):
        try:

            cfg = project.find_config_file()
            vfiles = project.collect_versioned_files(cfg)
            current_version = project.assert_versions(vfiles)

            # generate format
            kwargs['formatter'] = format_factory(cargs.get('--format'))
            kwargs['current_version'] = current_version

            return func(vfiles, cargs, *args, **kwargs)

        except project.ConfigurationError as config_err:
            print(str(config_err))

        except project.VersionMissMatchError as version_err:  # pragma: no cover
            print(str(version_err))

        except Exception as ex:  # pragma: no cover  pylint: disable=broad-except
            print("Error: {}".format(ex))

            if cargs['--debug'] is True:
                import traceback
                exc = sys.exc_info()
                traceback.print_tb(exc[2])

            sys.exit(1)

    return _command


@command
def version(*args, **kwargs):
    '''
    Return the raw version number string.

    '''
    cargs = args[1]
    version_str = kwargs['current_version']
    if cargs['--format']:
        # reformat this output to match format
        current_version = Version(version_str)
        version_str = kwargs['formatter'](current_version)

    print(version_str)


@command
def display(vfiles, cargs, **kwargs):
    '''
    Return the version number sting, as well as a listing
    of all the files with version strings and what that
    version number is.

    '''
    version_str = kwargs['current_version']
    if cargs['--format']:
        # reformat this output to match format
        version_str = kwargs['formatter'](Version(version_str))

    print('Current Version: {}'.format(version_str))
    print('Files:')
    project.print_versioned_lines(vfiles)


@command  # noqa: C901
def increment(vfiles, cargs, **kwargs):
    current_version = kwargs['current_version']
    new_version = Version(current_version)

    part = None

    if cargs['--major']:
        part = Version.MAJOR
    elif cargs['--minor']:
        part = Version.MINOR
    elif cargs['--patch']:
        part = Version.PATCH

    prerelease = PRState.null

    if cargs['--dev']:
        prerelease = PRState.dev
    elif cargs['--alpha']:
        prerelease = PRState.alpha
    elif cargs['--beta']:
        prerelease = PRState.beta
    elif cargs['--rc']:
        prerelease = PRState.rc
    elif cargs['--release']:
        prerelease = PRState.release

    new_version.increment(part, prerelease)

    new_version_str = kwargs['formatter'](new_version)

    print('Current Version: {}'.format(current_version))
    print('New Version:     {}'.format(new_version_str))

    if not cargs['--no-list']:
        print('Files:')
        project.print_versioned_updates(vfiles, new_version_str)

    if cargs['--apply'] is True:
        for vfile in vfiles:
            vfile.update(new_version_str)
            vfile.save()
        print('Version updates applied.')
