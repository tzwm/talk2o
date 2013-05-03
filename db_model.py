from google.appengine.ext import db

class Account(db.Model):
	email = db.StringProperty(required=True)
	actoken_key = db.StringProperty()
	actoken_secret = db.StringProperty()
	createdtime = db.DateTimeProperty(auto_now_add=True)
	updatedtime = db.DateTimeProperty(auto_now=True)


