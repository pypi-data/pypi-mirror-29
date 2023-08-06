from setuptools import setup

from itertools import chain

version = __import__('packy_agent').__version__

# These packages are auto installed along with virtualenv creation
# pip==9.0.1
# setuptools==36.0.1
# wheel==0.29.0

# This dependency enumeration is required to maintain strict versions of libraries used
# More detailed explanation could be found here:
# https://dmugtasimov-tech.blogspot.ru/2016/12/strict-dependencies.html

PIP = ('pip==9.0.1',)  # used in source code
PYTZ = ('pytz==2017.2',)
CERTIFI = ('certifi==2017.4.17',)
PYPARSING = ('pyparsing==2.2.0',)
PYYAML = ('PyYAML==3.12',)
GEVENT = ('gevent==1.2.2', 'greenlet==0.4.12')
ATOMICWRITES = ('atomicwrites==1.1.5',)
CACHETOOLS = ('cachetools==2.0.0',)
PYTHON_DATEUTIL = ('python-dateutil==2.6.1',)

CELERY = ('celery==4.1.0', 'amqp==2.2.2', 'billiard==3.5.0.3', 'kombu==4.1.0', 'vine==1.1.4') + PYTZ
REQUESTS = ('requests==2.18.4', 'chardet==3.0.4', 'idna==2.6', 'urllib3==1.22') + CERTIFI
ITSDANGEROUS = ('itsdangerous==0.24',)
SPEEDTEST_CLI = ('speedtest-cli==1.0.7',)
SUPERVISOR = ('supervisor==3.3.3', 'meld3==1.0.2')
JINJA = ('Jinja2==2.9.6',)
NETIFACES = ('netifaces==0.10.6',)
TAILER = ('tailer==0.4.1',)
UWSGI = ('uWSGI==2.0.15',)
UPTIME = ('uptime==3.0.1',)
SCHEMATICS = ('schematics==2.0.1',)
PYCURL = ('pycurl==7.43.0',)
RETRY = ('retry==0.9.2',)
PSUTIL = ('psutil==5.4.0',)

FLASK = ('Flask==0.12.2', 'click==6.7', 'MarkupSafe==1.0',
         'Werkzeug==0.12.2') + ITSDANGEROUS + JINJA
FLASK_WTF = ('Flask-WTF==0.14.2',) + FLASK

install_requires = list(set(chain(
    CELERY, REQUESTS, PYPARSING, PYYAML, FLASK, FLASK_WTF, SPEEDTEST_CLI, GEVENT,
    ATOMICWRITES, CACHETOOLS, SUPERVISOR, JINJA, PIP, NETIFACES, TAILER, UWSGI, UPTIME,
    PYTHON_DATEUTIL, SCHEMATICS, RETRY, PSUTIL
)))

setup(
    name='packy-agent',
    version=version,
    description='Packy Agent',
    packages=['packy_agent'],
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'post': list(PYCURL)
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'control-server = packy_agent.control_server.run:entry',
            'packy-watchdog = packy_agent.watchdog.run:entry',
            'print-initd-script = packy_agent.cli.print_initd_script:entry',
            'packy-agent-activate = packy_agent.cli.activate:entry',
        ]
    }
)
