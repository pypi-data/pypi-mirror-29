import sys
import argparse

from packy_agent.utils.logging import KNOWN_LOG_LEVELS, configure_basic_logging
from packy_agent.modules.http.base import get_http_measurement


def entry():
    from packy_agent.cli import activate as the_module
    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('url')
    parser.add_argument('--follow-redirects', action='store_true')
    parser.add_argument('--log-level', default='ERROR', choices=KNOWN_LOG_LEVELS)
    args = parser.parse_args()

    configure_basic_logging(level=args.log_level)

    url = args.url
    print 'Getting information for {}'.format(url)
    print get_http_measurement(url, follow_redirects=args.follow_redirects).to_json()

if __name__ == '__main__':
    sys.exit(entry())
