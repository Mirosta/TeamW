import cgi
import urllib

import webapp2

from google.appengine.ext import ndb

class User (ndb.Model):
    userName = ndb.StringProperty()
    name = ndb.StringProperty()
    password = ndb.StringProperty()
    dateOfBirth = ndb.DateProperty()

    def retrieveUser(self, key):
        user = key.get()
        return user

    def retrieveUserName(self, key):
        user = key.get()
        return user.userName



