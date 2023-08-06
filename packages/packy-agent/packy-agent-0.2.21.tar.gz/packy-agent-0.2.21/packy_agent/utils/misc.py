from __future__ import absolute_import

import logging
import random
import os
import os.path
import netifaces
import platform
import distutils.spawn
import datetime
import pytz
import dateutil.parser

from atomicwrites import AtomicWriter, atomic_write as atomic_write_original

UBUNTU_16_04_XENIAL = ('Ubuntu', '16.04', 'xenial')
LINUXMINT_18_1_SERENA = ('LinuxMint', '18.1', 'serena')

EPOCH_START_DATETIME = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)


logger = logging.getLogger(__name__)


def get_executable_path(executable, self_failover=True):
    path = distutils.spawn.find_executable(executable)
    if not path and self_failover:
        path = executable

    return path


def get_operating_system():
    try:
        return platform.linux_distribution()
    except Exception:
        # in case someone run it not on linux
        return None


def get_interfaces():
    return netifaces.interfaces()


def is_inside_docker_container():
    return os.path.isfile('/.dockerenv')


class CustomAtomicWriter(AtomicWriter):
    def commit(self, f):
        path = self._path
        if os.path.isfile(path):
            filestat = os.stat(path)
        else:
            filestat = None

        super(CustomAtomicWriter, self).commit(f)

        if filestat is not None:
            try:
                os.chmod(path, filestat.st_mode)
                os.chown(path, filestat.st_uid, filestat.st_gid)
            except Exception:
                logger.warning('Failed to restore permissions or ownership for file: %s', path)


def atomic_write(path, writer_cls=CustomAtomicWriter, **cls_kwargs):
    return atomic_write_original(path=path, writer_cls=writer_cls, **cls_kwargs)


# TODO(dmu) MEDIUM: Use `packy_agent.utils.shell.run_command` instead?
# TODO(dmu) MEDIUM: Provide logging to file for running shell commands
def run_shell_command_async(command, delay_seconds=None, dev_null=False):
    if delay_seconds is None:
        command = '({}) &'.format(command)
    else:
        command = '(sleep {}; {}) &'.format(delay_seconds, command)

    if dev_null:
        command = '({}) > /dev/null 2>&1'.format(command)

    logger.debug('Started async shell command: %s', command)
    os.system(command)
    logger.debug('Finished async shell command: %s', command)


def generate_random_string(size):
    return '%0x' % random.getrandbits(size * 4)


def get_iso_format_utcnow():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def to_epoch(dt):
    return (dt - EPOCH_START_DATETIME).total_seconds()


def iso_to_datetime(dt_string):
    return dateutil.parser.parse(dt_string)
