from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class RootHandler(webapp.RequestHandler):
    def get(self):
    	user = users.get_current_user()
    	if user:
    		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
    					(user.nickname(), users.create_logout_url("/")))
    	else:
    		greeting = ("<a href=\"%s\">Sign in</a>" % 
    					users.create_login_url("/"))

    	self.response.out.write("<html><body>%s</body></html>" % greeting)

    			
