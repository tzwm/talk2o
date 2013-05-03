import lib.twitter

import webapp2

from google.appengine.api import xmpp
from google.appengine.api import users
from google.appengine.ext import db
 

import db_model

class MainPage(webapp2.RequestHandler):

    def post(self):
        message = xmpp.Message(self.request.POST)

        user = db_model.Account(email=message.sender)
        user.put()

        users = db.GqlQuery("SELECT * FROM Account", email=message.sender)
        message.reply(str(users.count()))
        for user in users:
          message.reply(str(user.createdtime))

        
app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', MainPage)],
                              debug=True)
                              