
from payme.model.user import User
from payme.model.debt import Debt
from payme.model.payment import Payment
from payme.model.group import Group
from datetime import date
from payme.controller.contentHandler import PageHandler

from google.appengine.ext import ndb

class TestPage(PageHandler):

    def __init__(self):
        super(TestPage, self).__init__('testingPage')
        self.output = ''

#   MAIN
    def getHTML(self, controller, parameter):
        self.output += "Starting... <br>"

#   TEST 1 - Users
#        self.createUsers()

#   TEST 2 - Debts
#        self.createDebts()()
#        self.viewDebts()

#   TEST 3 - Payments
#
#         john = User.query(User.googleID == 'john').fetch(10)[0]
#         david = User.query(User.googleID == 'david').fetch(10)[0]
#
#         debt = Debt.query(Debt.creditor == david.key).fetch(10)[0]
#
#         self.createPayments(john.key, debt.key, 100)
#
#         self.viewDebts()

#   TEST 4 - Group and group debts

        self.createDebtGroup()


#   LEAVE THIS ALONE!
        return super(TestPage, self).getHTML(controller, parameter)

#   Create new single user and returns it
    def createUser(self, userName, name, year, mth, day):

        # u = User(id=userName, userName=userName, name=name, dateOfBirth=date(year, mth, day))
        u = User(googleID=userName, email='cock@email.com', dateOfBirth=date(year, mth, day), name=name)
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
        self.createUser('alison', 'Alison Burgers', 1991, 11, 12)
        self.createUser('dingdong', 'Ding Dong', 1990, 01, 23)

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

#   CHECKED - 5: Create and verify group
    def createDebtGroup(self):

        john = User.query(User.googleID == 'john').fetch(10)[0]
        david = User.query(User.googleID == 'david').fetch(10)[0]
        dingdong = User.query(User.googleID == 'dingdong').fetch(10)[0]

        # g = Group(name='Wolfpack')
        # g.put()
        # g = Group.query(Group.name == 'Wolfpack').fetch(10)[0]
        #
        # g.addUser(john.key)
        # g.addUser(david.key)
        #
        # d = Debt(creditor=dingdong.key, amount=8000)
        #
        #
        # g.addDebtEven(d)

        self.output += "John's OE: "
        self.output += str(john.getOE())

        self.output += "<br>David's OE: "
        self.output += str(david.getOE())

        self.output += "<br>Dingdong's OE: "
        self.output += str(dingdong.getOE())