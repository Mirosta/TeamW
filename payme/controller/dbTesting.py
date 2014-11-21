
from usertest import User
from datetime import date
from payme.controller.contentHandler import PageHandler

class TestPage(PageHandler):

    def __init__(self):
        super(TestPage, self).__init__('testingPage')
        self.output = ''

    def getHTML(self, controller, parameter):
        u = User(userName='john', name='John Smith', password='pass', dateOfBirth=date(1993, 12, 22))
        key = u.put() # put returns key to u in the database
        self.output = User.retrieveUserName(u, key)
        return super(TestPage, self).getHTML(parameter)