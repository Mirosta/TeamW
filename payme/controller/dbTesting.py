from payme.controller.globals import Global
from payme.model.user import User
from payme.model.debt import Debt
from payme.model.payment import Payment
from payme.model.group import Group
from payme.model.notification import Notification

from datetime import date, datetime
from payme.controller.contentHandler import PageHandler

from payme.controller.globals import Global

import json

from google.appengine.ext import ndb

class TestPage(PageHandler):

    def __init__(self):
        super(TestPage, self).__init__('testingPage')
        self.output = ''

    # Get key for the current user
    def getCurrentUser(self):
        return Global.controller.getCurrentUser()

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
        # john = self.queryUser('john')
        # david = self.queryUser('david')
        # dingdong = self.queryUser('dingdong')
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

        # john = self.createUser('john', "John Smith")
        # david = self.createUser('david', "David Hutchinson")
        # dingdong = self.createUser('dingdong', "Ding Dong")
        #
        # debt = self.createDebt(dingdong.key, john.key, 5000)
        #
        # payment = self.createPayments(john.key, debt.key, 300)

        # group = self.createNewGroup('Wolfpack')

        # group = Group.query(Group.name == 'Wolfpack').fetch()[0]

        # john.addGroup(group.key)
        # dingdong.addGroup(group.key)

        # group.addMember(dingdong.key)

        # self.output += "<br>" + self.serialize(group)

#
# #         CREATE STUFF!! - ONLY RUN ONCE
#
#         self.output += 'Creating users... <br>'
#         john = self.createUser('john', "John Smith")
#         david = self.createUser('david', "David Hutchinson")
#         dingdong = self.createUser('dingdong', "Ding Dong")
#
#         self.output += 'Creating group, Wolfpack... <br>'
#         group = self.createNewGroup('Wolfpack')
#
#         self.output += 'Creating debt (Dingdong to John)... <br>'
#         debt = self.createDebt(dingdong.key, john.key, 5000)
#
#         self.output += 'Creating payments... <br>'

        # payment = self.createPayments(john.key, debt.key, 300)
#
#         self.output += 'Create notifications... <br><br>'
#         notification1 = self.createNotification(Notification.Type.INFO, 'Test notification 1')
#         notification2 = self.createNotification(Notification.Type.INFO, 'Test notification 2')
#         notification3 = self.createNotification(Notification.Type.INFO, 'Test notification 3')
#
# #         ASSOCIATE STUFF!! - ONLY RUN ONCE
#
# #         Add friends
#         self.output += 'Adding David and Dingdong to John... <br>'
#         john.addFriend(david.key)
#         john.addFriend(dingdong.key)
#
# #         Add group
#         self.output += 'Adding Wolpack to John <br>'
#         john.addGroup(group.key)
#
# #         Add member of the group
#         self.output += 'Adding Dingdong to John\'s Wolfpack...<br>'
#         group.addMember(dingdong.key)
#
# #           Give John notification
#         self.output += 'Sending John notification...<br>'
#         john.giveNotification(notification1.key)
#         john.giveNotification(notification2.key)
#         david.giveNotification(notification3.key)
#
#         self.output += 'Done... <br>'
#         # self.output += "<br>" + self.serialize(group)

        # john = self.queryUser('john')
        # dingdong = self.queryUser('dingdong')

        # alex = self.createUser('alex', "Alex Peterson")
        # dingdong = self.queryUser('alex')
        # alex.key.delete()

        # self.output += str(getattr(alex, 'name'))

        # self.createDebt(alex.key, john.key, 5000)

        # debt = Debt.query(Debt.creditor == dingdong.key).fetch()[0]
        # self.output += self.serialize(debt)
        #
        # debt.update({'disputed': True})

        # alex = self.queryUserByName('Alex')
        pollawat = self.queryUserByName('Pollawat')
        tom = self.queryUserByName('Thomas')
        john = self.queryUserByName('John Smith')

        # pollawat.addFriend(alex.key)
        # alex.addFriend(pollawat.key)

        # debt = Debt.query(Debt.creditor == alex.key, Debt.debtor == pollawat.key).fetch()[0]

        # debt = Debt.query(Debt.creditor == pollawat.key).fetch()[0]

        # jim = self.createUser('jim', 'Jim')

        # jim = self.queryUser('jim')

        # arthur = self.createUser('arthur', 'Arthur')

        # arthur = self.queryUser('arthur')
        # arthur.addFriendForce(pollawat.key)

        # james = self.createUser('james', 'James')
        # james.addFriendForce(tom.key)

        debt = self.createDebt(john.key, self.getCurrentUser().key, 2000)

        # self.createPayments(john.key, debt.key, 10)

        # payment = self.createPayments(pollawat.key, debt.key, 10)

        # payment = Payment.query(Payment.payer == pollawat.key).fetch()[0]

        # payment.update({'disputed': True})

        # self.createDebt(alex.key, pollawat.key, 100)

        # self.output += str(getattr(alex, 'name'))
        # debt.notifyDebtor()

        # alex.update({'name': 'Alex A Peterson'})

        # debt = self.createDebt(dingdong.key, john.key, 5000)

        # debt = Debt.query(Debt.creditor == dingdong.key).fetch()[0]
        # payment = Payment.query(Payment.payer == john.key).fetch()[0]

        # payment.raiseDispute()

        # debt.removeMe()

#   LEAVE THIS ALONE!
        return super(TestPage, self).getHTML(controller, parameter)

    def queryUser(self, key):
        user = User.query(User.googleID == key).fetch(10)

        if user.__len__() != 0:
            return user[0]
        else:
            return '{error: "User not found"}'

    def queryUserByKey(self, key):
        user = User.query(User.key == key).fetch(10)

        if user.__len__() != 0:
            return user[0]
        else:
            return '{error: "User not found"}'


    def queryUserByName(self, key):
        user = User.query(User.name == key).fetch(10)

        if user.__len__() != 0:
            return user[0]
        else:
            return '{error: "User not found"}'

#   Create new single user and returns it
    def createUser(self, userName, name):

        # u = User(id=userName, userName=userName, name=name, dateOfBirth=date(year, mth, day))
        u = User(googleID=userName, email='cock@email.com', name=name)
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

    def createNewGroup(self, name):
        g = Group(name=name)
        g.put()

        return g

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

    def createNotification(self, type, content):
        n = Notification(type=type, content=content)
        n.put()

        return n

class JSonAPIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return obj.strftime(Global.JSONDateTime)
        elif isinstance(obj, ndb.Key):
            return obj.urlsafe()
        elif isinstance(obj, ndb.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)
