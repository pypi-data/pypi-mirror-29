import argparse

from packy_agent.watchdog.service import WatchdogService


def entry():
    from packy_agent.watchdog import run as the_module

    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.parse_args()

    service = WatchdogService()
    service.run()


if __name__ == '__main__':
    entry()
