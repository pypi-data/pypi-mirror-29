from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)


def write_to_console_or_file(target, content):
    if target == '-':
        print content
    else:
        logger.info('Writing content to %s:\n%s', target, content)
        # TODO(dmu) MEDIUM: Consider using atomic writes
        with open(target, 'w') as f:
            f.write(content)
        logger.info('Written content to %s', target)
