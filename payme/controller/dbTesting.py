
from usertest import User
from datetime import date
from payme.controller.contentHandler import PageHandler
from google.appengine.ext import ndb

class TestPage(PageHandler):

    def __init__(self):
        super(TestPage, self).__init__('testingPage')
        self.output = ''

    def createUser(self, userName, name, year, mth, day):
        u = User(id=userName, userName=userName, name=name, dateOfBirth=date(year, mth, day))
        u.put()

    def getHTML(self, controller, parameter):

        self.createUser('david', 'David Hutchinson', 1993, 01, 01)
        self.createUser('john', 'John Smith', 1993, 01, 02)

        users = User.query(User.userName == 'john').fetch(100)

        for user in users:
            self.output += user.retrieveUserName()

        return super(TestPage, self).getHTML(controller, parameter)
