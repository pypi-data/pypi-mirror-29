from __future__ import absolute_import

import functools
from packy_agent.configuration.agent.base import configuration as agent_configuration
from flask import session, redirect, request, url_for


def is_activated():
    return agent_configuration.is_activated()


def is_authenticated():
    agent_id = session.get('agent_id')
    if agent_id is not None:
        return agent_configuration.get_agent_id() == agent_id
    return False


def set_authentication_cookie():
    agent_id = agent_configuration.get_agent_id()
    if agent_id is not None:
        session['agent_id'] = agent_id


def login():
    set_authentication_cookie()


def logout():
    session.pop('agent_id', None)


def activation_and_authentication_required(func_or_method):
    @functools.wraps(func_or_method)
    def wrapper(*args, **kwargs):
        if not is_activated():
            return redirect(url_for('activate'))
        elif not is_authenticated():
            return redirect(url_for('login') + '?next=' + request.path)
        else:
            return func_or_method(*args, **kwargs)

    return wrapper


def activation_required(func_or_method):
    @functools.wraps(func_or_method)
    def wrapper(*args, **kwargs):
        if not is_activated():
            return redirect(url_for('activate'))
        else:
            return func_or_method(*args, **kwargs)

    return wrapper
