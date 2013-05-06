from google.appengine.ext import db

class Client(db.Model):
	email = db.StringProperty(required=True)
	twitter_actoken_key = db.StringProperty()
	twitter_actoken_secret = db.StringProperty()
	createdtime = db.DateTimeProperty(auto_now_add=True)
	updatedtime = db.DateTimeProperty(auto_now=True)


