from __future__ import absolute_import

import logging
from operator import itemgetter

from logging import _levelNames

KNOWN_LOG_LEVELS = tuple(
    v for k, v in sorted(_levelNames.iteritems(), key=itemgetter(0)) if isinstance(v, basestring))

BASIC_LOGGING_FORMAT = '%(asctime)-15s %(levelname)s [%(name)s]: %(message)s'


def configure_basic_logging(format=BASIC_LOGGING_FORMAT, level=logging.DEBUG):
    logging.basicConfig(format=format, level=level)
