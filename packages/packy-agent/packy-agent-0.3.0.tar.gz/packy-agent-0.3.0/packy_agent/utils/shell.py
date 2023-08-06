from __future__ import absolute_import

import logging
import subprocess

logger = logging.getLogger(__name__)


def run_command(command, raise_exception=False):
    logger.info('Running shell command: %s', command)
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as ex:
        logger.error('Shell command failed: %s: %s', command, ex.output.strip())
        if raise_exception:
            raise
    else:
        logger.info('Shell command succeeded: %s: %s', command, output.strip())
        return output


def install_ubuntu_packages(packages, one_command=True):
    run_command('apt-get update')
    if one_command:
        run_command('apt-get install -y {}'.format(' '.join(packages)))
    else:
        for package in packages:
            run_command('apt-get install -y {}'.format(package))


def install_alpine_packages(packages, one_command=True):
    run_command('apk update')
    if one_command:
        run_command('apk add {}'.format(' '.join(packages)))
    else:
        for package in packages:
            run_command('apk add {}'.format(package))
