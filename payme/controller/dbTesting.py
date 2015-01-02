
from payme.model.user import User
from payme.model.debt import Debt
from payme.model.payment import Payment
from datetime import date
from payme.controller.contentHandler import PageHandler

from google.appengine.ext import ndb

class TestPage(PageHandler):

    def __init__(self):
        super(TestPage, self).__init__('testingPage')
        self.output = ''

#   MAIN
    def getHTML(self, controller, parameter):
        self.output += "Starting..."

#   TEST 1 - Users
#        self.createUsers()

#   TEST 2 - Debts
#        self.createDebts()()
#        self.viewDebts()

#   TEST 3 - Payments

        john = User.query(User.googleID == 'john').fetch(10)[0]
        david = User.query(User.googleID == 'david').fetch(10)[0]

        debt = Debt.query(Debt.creditor == david.key).fetch(10)[0]

        self.createPayments(john.key, debt.key, 100)

        self.viewDebts()

        return super(TestPage, self).getHTML(controller, parameter)

#   Create new single user and returns it
    def createUser(self, userName, name, year, mth, day):

        # u = User(id=userName, userName=userName, name=name, dateOfBirth=date(year, mth, day))
        u = User(googleID=userName, email='cock@email.com', dateOfBirth=date(year, mth, day), firstName=name)
        u.put()

        return u

#   Create new debt and returns it
    def createDebt(self, creditor, debtor, amount):
        d = Debt(creditor=creditor, debtor=debtor, amount=amount)
        d.put()

        return d

#   CHECKED - 1: Add specimen users to database
    def createUsers(self):
        self.createUser('david', 'David Hutchinson', 1993, 01, 01)
        self.createUser('john', 'John Smith', 1993, 01, 02)

        users = User.query(User.googleID == 'john').fetch(100)

        for user in users:
            self.output += user.retrieveUserName()

#   CHECKED - 2: Add debts to database
    def createDebts(self):
        david = self.createUser('david', 'David Hutchinson', 1993, 01, 01)
        john = self.createUser('john', 'John Smith', 1993, 01, 02)

        self.createDebt(david.key, john.key, 2000)

#   CHECKED - 3: View debt
    def viewDebts(self):
        john = User.query(User.googleID == 'john').fetch(100)
        self.output += str(john[0].getOE())

#   CHECKED - 4: Create new payments
    def createPayments(self, payer, debt, amount):
        p = Payment(payer=payer, debt=debt, amount=amount)
        p.put()

        return p


