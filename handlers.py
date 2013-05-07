from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db

import urlparse
from webapp2_extras import sessions
import webapp2

import lib.oauth2 as oauth
import db_model
import config

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):                                 # override dispatch
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)       # dispatch the main handler
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class RootHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))

            clients = db.GqlQuery("SELECT * FROM Client", email=user.email())
            if not clients.get():
                client = db_model.Client(email=user.email())
                client.put()
                clients.get()
                self.redirect('/')


            twitter_actoken_key = clients.get().twitter_actoken_key
            twitgreeting = ""
            if twitter_actoken_key:
                twitgreeting = ("twitter auth ok.")
            else:
                twitgreeting = ('<a href="/twitter/oauth/">twitter:sign in</a>')
        else:
            greeting = ("<a href=\"%s\">Sign in</a>" % 
                        users.create_login_url("/"))
            twitgreeting = ""

        self.response.out.write("<html><body>%s<br>%s</body></html>" % (greeting, twitgreeting))


class TwitterHandler(BaseHandler):
    def auth(self):
        consumer = oauth.Consumer(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        client = oauth.Client(consumer)

        resp, content = client.request(config.REQUEST_TOKEN_URL, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])
        request_token = dict(urlparse.parse_qsl(content))

        self.session['req_token'] = request_token

        self.redirect('%s?oauth_token=%s' % (config.AUTHORIZE_URL, request_token['oauth_token']))


    def callback(self):
        verifier = self.request.get('oauth_verifier')
        request_token = self.session.pop('req_token', None)
        token = oauth.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
        token.set_verifier(verifier)
        consumer = oauth.Consumer(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        client = oauth.Client(consumer, token)

        resp, content = client.request(config.ACCESS_TOKEN_URL, "POST")
        access_token = dict(urlparse.parse_qsl(content))

        user = users.get_current_user()
        clients = db.GqlQuery("SELECT * FROM Client", email=user.email())
        client = clients.get()
        client.twitter_actoken_key = access_token['oauth_token']
        client.twitter_actoken_secret = access_token['oauth_token_secret']
        client.put()

        self.redirect('/')