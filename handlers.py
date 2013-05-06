from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db

import urlparse

import lib.oauth2 as oauth
import db_model
import config

# twitgreeting = "test"
# twitvisit = "test"

class RootHandler(webapp.RequestHandler):
    def get(self):
    	# global twitgreeting, twitvisit

    	user = users.get_current_user()
    	if user:
    		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
    					(user.nickname(), users.create_logout_url("/")))

    		clients = db.GqlQuery("SELECT * FROM Client", email=user.email())
    		if not clients.get():
    			client = db_model.Client(email=user.email())
    			client.put()
    			clients.fetch()

			twitter_actoken_key = clients.get().twitter_actoken_key
			twitter_actoken_secret = clients.get().twitter_actoken_secret
			
			if twitter_actoken_key:
				twitgreeting = ("ok, %s." % twitter_actoken_key)
			else:
				consumer - oauth.Consumer(config.CONSUMER_KEY, config.CONSUMER_SECRET)
				client = oauth.Client(consumer)

				resp, content = client.request(config.REQUEST_TOKEN_URL, "GET")
				if resp['status'] != '200':
					raise Exception("Invalid response %s." % resp['status'])
				request_token = dict(urlparse.parse_qsl(content))

				twitvisit = ("%s?oauth_token=%s" % (config.AUTHORIZE_URL, request_token['oauth_token']))
				twitgreeting = ("to authenticate")
    	else:
    		greeting = ("<a href=\"%s\">Sign in</a>" % 
    					users.create_login_url("/"))

    	self.response.out.write("<html><body>%s<br>%s<br>%s</body></html>" % (greeting, twitgreeting, twitvisit))

    			
