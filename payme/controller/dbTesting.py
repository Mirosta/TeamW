
from payme.model.user import User
from payme.model.debt import Debt
from payme.model.payment import Payment

from datetime import date, datetime
from payme.controller.contentHandler import PageHandler

import json

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

#  TEST 3 - Payments

        # john = self.queryUser('john')
        # david = self.queryUser('david')
        # dingdong = self.queryUser('dingdong')
        #
        # debt = Debt.query(Debt.creditor == dingdong.key).fetch(10)[0]
        #
        # self.createPayments(john.key, debt.key, 100)
        #
        # self.viewDebts()

#   TEST 4 - Group and group debts

#         self.createDebtGroup()
#
# #   TEST 5 - Add friends
#
#         john = self.queryUser('john')
#         david = self.queryUser('david')
#         dingdong = self.queryUser('dingdong')
#
#         # john.addFriend(david.key)
#         # john.addFriend(dingdong.key)
#
#         # self.output += str(john.friends)
#         self.output = self.serialize(john)
#
#         self.output += "<br>"
#
#         # self.createDebt(dingdong.key, john.key, 5000)
#
#         debt = Debt.query(Debt.creditor == dingdong.key).fetch(10)[0]
#
#         # self.createPayments(john.key, debt.key, 1000)
#         self.viewDebts()

        john = self.createUser('john', "John Smith")
        david = self.createUser('david', "David Hutchinson")
        dingdong = self.createUser('dingdong', "Ding Dong")

        debt = self.createDebt(dingdong, john, 5000)


#   LEAVE THIS ALONE!
        return super(TestPage, self).getHTML(controller, parameter)

    def queryUser(self, key):
        user = User.query(User.googleID == key).fetch(10)

        if user.__len__() != 0:
            return user[0]
        else:
            return '{error: "User not found"}'

#   Create new single user and returns it
    def createUser(self, userName, name):

        # u = User(id=userName, userName=userName, name=name, dateOfBirth=date(year, mth, day))
        u = User(googleID=userName, email='cock@email.com')
        u.put()

        return u

#   Create new debt and returns it
    def createDebt(self, creditor, debtor, amount):
        d = Debt(creditor=creditor, debtor=debtor, amount=amount)
        d.put()

        return d

#   CHECKED - 1: Add specimen users to database
    def createUsers(self):
        self.createUser('david', 'David Hutchinson')
        self.createUser('john', 'John Smith')
        self.createUser('alison', 'Alison Burgers')
        self.createUser('dingdong', 'Ding Dong')

        users = User.query(User.googleID == 'john').fetch(100)

        for user in users:
            self.output += user.retrieveUserName()

#   CHECKED - 2: Add debts to database
    def createDebts(self):
        david = self.createUser('david', 'David Hutchinson')
        john = self.createUser('john', 'John Smith')

        self.createDebt(david.key, john.key, 2000)

#   CHECKED - 3: View debt
    def viewDebts(self):
        john = self.queryUser('john')
        self.output += str(john.getOE())

#   CHECKED - 4: Create new payments
    def createPayments(self, payer, debt, amount):
        p = Payment(payer=payer, debt=debt, amount=amount)
        p.put()

        return p

    def serialize(self, object_to_serialize):
        return json.dumps(object_to_serialize, cls=JSonAPIEncoder)

#   CHECKED - 5: Create and verify group
    def createDebtGroup(self):

        john = self.queryUser('john')
        david = self.queryUser('david')
        dingdong = self.queryUser('dingdong')

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

        # self.output += "John's OE: "
        # self.output += str(john.getOE())
        #
        # self.output += "<br>David's OE: "
        # self.output += str(david.getOE())
        #
        # self.output += "<br>Dingdong's OE: "
        # self.output += str(dingdong.getOE())

        self.output += "<br>"
        self.output += str(self.serialize(john))


#
class JSonAPIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return obj.strftime('%Y/%m/%d %H:%M:%S')
        elif isinstance(obj, ndb.Key):
            return str(obj)
        elif isinstance(obj, ndb.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)
