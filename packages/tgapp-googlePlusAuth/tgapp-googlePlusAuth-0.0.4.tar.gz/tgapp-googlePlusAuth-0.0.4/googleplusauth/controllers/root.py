# -*- coding: utf-8 -*-
"""Main Controller"""
from tg import TGController, config, hooks
from tg import expose, flash, redirect
from tg.i18n import ugettext as _
import json
from googleplusauth import model
from googleplusauth.lib.utils import redirect_on_fail, login_user, has_googletoken_expired, add_param_to_query_string
from tgext.pluggable import app_model
from datetime import datetime
from six.moves.urllib.request import urlopen


class RootController(TGController):
    @expose()
    def login(self, token, came_from=None, remember=None):
        gplusanswer = urlopen('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s' % token)
        google_id = None
        google_token_expiry = None
        google_email = None
        answer = None

        try:
            answer = json.loads(gplusanswer.read().decode('utf-8'))
            if answer['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                flash(_("Login error"), "error")
                return redirect_on_fail()
            if not answer['sub']:
                flash(_("Login error"), "error")
                return redirect_on_fail()

            google_id = answer['sub']
            google_token_expiry = datetime.fromtimestamp(int(answer['exp']))

        except Exception:
            flash(_('Fatal error while trying to contact Google'), 'error')
            return redirect_on_fail()
        finally:
            gplusanswer.close()

        ga_user = model.GoogleAuth.ga_user_by_google_id(google_id)

        if ga_user:
            #If the user already exists, just login him.
            login_user(ga_user.user.user_name, remember)

            if has_googletoken_expired(ga_user):
                ga_user.access_token = token
                ga_user.access_token_expiry = google_token_expiry

            hooks.notify('googleplusauth.on_login', args=(answer, ga_user.user))
            redirect_to = add_param_to_query_string(config.sa_auth['post_login_url'], 'came_from', came_from)

            return redirect(redirect_to)

        # User not present
        user_dict = dict(
            user_name='g+:%s' % google_id,
            email_address=answer['email'],
            password=token,
            display_name=answer['name']
        )
        #  Create new user
        hooks.notify('googleplusauth.on_registration', args=(answer, user_dict))
        try:
            u = model.provider.create(app_model.User, user_dict)
        except:
            # clear the session so the user won't be created
            try:  # ming
                model.DBSession.clear()
            except:  # sqlalchemy
                model.DBSession.expunge_all()
            # query the user so it will be merged
            u = model.provider.get_obj(
                app_model.User,
                dict(email_address=user_dict['email_address'])
            )

        #  Create new Google Plus Login User for store data
        gpl = model.GoogleAuth(
            user=u,
            google_id=google_id,
            registered=True,
            just_connected=True,
            access_token=token,
            access_token_expiry=google_token_expiry,
            profile_picture=answer['picture']
        )


        #  Now login and redirect to request page
        login_user(u.user_name, remember)
        redirect_to = add_param_to_query_string(config.sa_auth['post_login_url'], 'came_from', came_from)

        return redirect(redirect_to)

    @expose()
    def login_error(self):
        flash(_("Login error"), "error")
        return redirect_on_fail()
