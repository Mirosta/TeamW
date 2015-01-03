import cgi
import urllib

from google.appengine.ext import ndb

class User (ndb.Model):
    userName = ndb.StringProperty()
    name = ndb.StringProperty()
    dateOfBirth = ndb.DateProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    def retrieveUserName(self):
        return self.userName