# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-googlePlusAuth."""
#  For more scope: https://developers.google.com/oauthplayground/

from markupsafe import Markup
from tg import request


def bold(text):
    return Markup('<strong>%s</strong>' % text)


def load_js_sdk():
    return '''<script src="https://apis.google.com/js/client:platform.js"></script>'''


def login_button(client_id, scope=None, data_cookiepolicy=None, img_btn_login=None, remember='', **kwargs):

    if not data_cookiepolicy:
        data_cookiepolicy = "single_host_origin"

    if not img_btn_login:
        img_btn_login = "https://developers.google.com/identity/images/sign-in-with-google.png"

    default_scope = "https://www.googleapis.com/auth/userinfo.email"
    if not scope:
        scope = default_scope
    else:
        scope += " "+default_scope
    html = '''
    <div id="button-container">
        <div id="google-login-button" style="cursor: pointer;" onclick="perform_google_login()">
            <img id="img-login" src='%(img_btn_login)s' alt='Google Login' />
        </div>
    </div>
    <script type="text/javascript">
    var auth2 = {};
    var helper = (function() {
      return {
        /**
         * Hides the sign in button and starts the post-authorization operations.
         *
         * @param {Object} authResult An Object which contains the access token and
         *   other authentication information.
         */
        onSignInCallback: function(authResult) {
          if (authResult.isSignedIn.get()) {
            $('#google-login-button').hide();
            helper.profile();
          } else if (authResult['error'] ||
              authResult.currentUser.get().getAuthResponse() == null) {
              // There was an error, which means the user is not signed in.
              var loginUrl = "/googleplusauth/login_error";
              window.location = loginUrl;
              $('#google-login-button').show();
          }
        },

        /**
         * Calls the OAuth2 endpoint to disconnect the app for the user.
         */
        disconnect: function() {
          // Revoke the access token.
          auth2.disconnect();
        },

        /**
         * Gets the currently signed in user's profile data.
         */

        profile: function(){
          var profile = auth2.currentUser.get().getBasicProfile();
          var token = auth2.currentUser.get().getAuthResponse().id_token;
          //send the token to server for validation
          var remember = "%(remember)s";
          var loginUrl = "/googleplusauth/login?token="+ token +"&came_from=%(came_from)s";
          if (remember){
              loginUrl += '&remember=' + remember;
          }
          window.location = loginUrl;
        }
      };
    })();


    /**
     * Handler for when the sign-in state changes.
     *
     * @param {boolean} isSignedIn The new signed in state.
     */
    var updateSignIn = function() {
      if (auth2.isSignedIn.get()) {
        helper.onSignInCallback(gapi.auth2.getAuthInstance());
      }else{
        helper.onSignInCallback(gapi.auth2.getAuthInstance());
      }
    }

    /**
     * This method sets up the sign-in listener after the  user click on the button.
     */
    var loaded = false;
    function perform_google_login() {
      gapi.load('auth2', function() {
          gapi.auth2.init({
              client_id: '%(client_id)s',
              fetch_basic_profile: true,
              cookie_policy: '%(data_cookiepolicy)s',
              scope:'%(scope)s'}).then(
                function (){
                  auth2 = gapi.auth2.getAuthInstance();
                  auth2.isSignedIn.listen(updateSignIn);
                  auth2.then(updateSignIn());
                  loaded=true;
                  if(!auth2.isSignedIn.get())
                    {
                      auth2.signIn();
                    }
                });
      });
      if(loaded == true) {
        auth2.signIn();
      }
    }
    </script>
        ''' % dict(img_btn_login=img_btn_login,
                   client_id=client_id,
                   data_cookiepolicy=data_cookiepolicy,
                   scope=scope,
                   remember=remember,
                   came_from=request.GET.get('came_from', '/'))

    script = load_js_sdk()

    return Markup(html + script)
