import cgi
import urllib

import webapp2

from google.appengine.ext import ndb

class User (ndb.Model):
    userName = ndb.StringProperty()
    name = ndb.StringProperty()
    password = ndb.StringProperty()
    dateOfBirth = ndb.DateTimeProperty()

    def createUser(self):
        u = User(userName='john', name='John Smith', password='pass', dateOfBirth = '01011993')
        k = u.put() # put returns key to u in the database

    def retrieveUser(self, key):
        user = key.get()

