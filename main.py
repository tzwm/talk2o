from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from webapp2 import WSGIApplication, Route

routes = [
  Route('/', handler='handlers.RootHandler')
]

app = WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    