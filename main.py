from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from webapp2 import WSGIApplication, Route

import config

routes = [
  Route('/_ah/xmpp/message/chat/', handler='xmpp_handler.XMPPHandler'),
  Route('/', handler='handlers.RootHandler'),
  Route('/twitter/oauth/', handler='handlers.TwitterHandler:auth'),
  Route('/twitter/callback/', handler='handlers.TwitterHandler:callback')
]

app_config = {
  'webapp2_extras.sessions':{
    'secret_key': config.SESSION_KEY
  }
}

app = WSGIApplication(routes, config=app_config, debug=True)



def main():

    run_wsgi_app(app)


if __name__ == '__main__':
    main()
    