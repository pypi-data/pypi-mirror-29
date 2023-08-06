# -*- coding: utf-8 -*-
import logging
import tg
from tgext.pluggable import PluggableSession, app_model

log = logging.getLogger('tgapp-tgappgooglePlusAuth')

DBSession = PluggableSession()
GoogleAuth = None


def init_model(app_session):
    DBSession.configure(app_session)


def import_models():
    global GoogleAuth
    if tg.config.get('use_sqlalchemy', False):
        from .sqla_models import GoogleAuth
    elif tg.config.get('use_ming', False):
        from .ming_models import GoogleAuth
        app_model.User.googleplusauth = property(
            lambda o: GoogleAuth.googleplusauth_user(o._id)
        )


class PluggableSproxProvider(object):
    def __init__(self):
        self._provider = None

    def _configure_provider(self):
        if tg.config.get('use_sqlalchemy', False):
            log.info('Configuring googlePlusAuth for SQLAlchemy')
            from sprox.sa.provider import SAORMProvider
            self._provider = SAORMProvider(session=DBSession)
        elif tg.config.get('use_ming', False):
            log.info('Configuring googlePlusAuth for Ming')
            from sprox.mg.provider import MingProvider
            self._provider = MingProvider(DBSession)
        else:
            raise ValueError('googlePlusAuth should be used with sqlalchemy or ming')

    def __getattr__(self, item):
        if self._provider is None:
            self._configure_provider()

        return getattr(self._provider, item)

provider = PluggableSproxProvider()
