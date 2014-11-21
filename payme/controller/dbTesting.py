
from usertest import User
from datetime import date
from payme.controller.contentHandler import PageHandler
from google.appengine.ext import ndb

class TestPage(PageHandler):

    def __init__(self):
        super(TestPage, self).__init__('testingPage')
        self.output = ''

    def getHTML(self, parameter):
        u1 = User(userName='john', name='John Smith', password='pass', dateOfBirth=date(1993, 12, 22))
        u1.put() # put returns key to u in the database

        u2 = User(userName='david', name='David Hutchinson', password='pass', dateOfBirth=date(1992, 12, 22))
        u2.put() # put returns key to u in the database

        key = ndb.Key(User, 'david')

        self.output = User.retrieveUserName(key)

        return super(TestPage, self).getHTML(parameter)
