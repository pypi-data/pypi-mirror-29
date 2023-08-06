# -*- coding: utf-8 -*-

import tg
from datetime import datetime
from six.moves.urllib.parse import urlparse, parse_qs, urlunparse
from six.moves.urllib.parse import urlencode


def redirect_on_fail():
    return tg.redirect(tg.request.referer or tg.config.sa_auth['post_logout_url'])


def login_user(user_name, expire=None):
    request = tg.request
    response = tg.response

    request.cookies.clear()
    authentication_plugins = request.environ['repoze.who.plugins']
    identifier = authentication_plugins['main_identifier']

    login_options = {'repoze.who.userid':user_name}
    if expire:
        login_options['max_age'] = expire

    if not request.environ.get('repoze.who.identity'):
        response.headers = identifier.remember(request.environ, login_options)


def has_googletoken_expired(user):
    expire = user.access_token_expiry
    if not expire:
        return True

    if datetime.now() > expire:
        return True

    return False


def add_param_to_query_string(url, param, value):
    url_parts = list(urlparse(url))
    query_parts = parse_qs(url_parts[4])
    query_parts[param] = value
    url_parts[4] = urlencode(query_parts, doseq=True)
    return urlunparse(url_parts)
