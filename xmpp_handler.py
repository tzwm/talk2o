from google.appengine.api import xmpp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
 
import config
import db_model
import lib.twitter as twitter

class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)

        clients = db.GqlQuery("SELECT * FROM Client", email=message.sender)
        if not clients.get():
            message.reply("Please visit https://tzwmtest.appspot.com/ to get start")
            return
        
        access_token_key = clients.get().twitter_actoken_key
        access_token_secret = clients.get().twitter_actoken_secret

        api = twitter.Api(consumer_key=config.CONSUMER_KEY,
                          consumer_secret=config.CONSUMER_SECRET,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)  
        api.PostUpdate(message.body)
