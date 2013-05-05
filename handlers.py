from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class RootHandler(webapp.RequestHandler):
    def get(self):
    	try:
            first = int(self.request.get('first'))
            second = int(self.request.get('second'))

            self.response.out.write("<html><body><p>%d + %d = %d</p></body></html>" %
                                    (first, second, first + second))
        except (TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid inputs</p></body></html>")