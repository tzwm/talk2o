import twitter

import webapp2

from google.appengine.api import xmpp

class MainPage(webapp2.RequestHandler):

    def post(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('Hello, webapp2 World!')
        api = twitter.Api(consumer_key='7F8OYpbHhV9Co1BOg9quzw',
                      consumer_secret='KsHFmzE6Lpze7lDNpbB0RnX5FmV3M2caV0SWv15uXo',
                      access_token_key='113048411-hRltQGjd4d6s8HlhtKYOe7KgtcyK1PQjhzae4yta',
                      access_token_secret='pWkq7TsGBaGZTZQs8KyvQk95TwjmZNgQq6Zb7zI')

        message = xmpp.Message(self.request.POST)
        api.PostUpdate(message.body)
        message.reply("ok")

        
app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', MainPage)],
                              debug=True)
                              