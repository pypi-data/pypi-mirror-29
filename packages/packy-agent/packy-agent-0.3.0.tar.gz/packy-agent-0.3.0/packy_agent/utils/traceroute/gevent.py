from __future__ import absolute_import

import sys
import select
import socket
from contextlib import contextmanager


def async_patch():
    from gevent import monkey

    monkey.patch_socket()
    monkey.patch_select()


def async_unpatch():
    reload(select)
    if sys.version_info[:2] >= (3, 4):
        import selectors
        reload(selectors)
    reload(socket)


@contextmanager
def async_patched():
    async_patch()
    try:
        yield
    except:
        raise
    finally:
        async_unpatch()
