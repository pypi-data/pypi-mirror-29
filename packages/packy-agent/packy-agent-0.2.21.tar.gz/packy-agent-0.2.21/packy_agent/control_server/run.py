import argparse

from packy_agent.control_server.app import get_app


def entry():
    from packy_agent.control_server import run as the_module

    parser = argparse.ArgumentParser(
        # Cannot use __name__, because when module is run as script it is equal to __main__
        prog='python -m {}'.format(the_module.__name__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8001)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--packy-server-base-url')

    args = parser.parse_args()

    app = get_app(packy_server_base_url=args.packy_server_base_url)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    entry()
