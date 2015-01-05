from payme.model.user import User
from payme.model.debt import Debt
from payme.model.payment import Payment
from payme.model.group import Group
from payme.model.notification import Notification
from payme.controller.contentHandler import PageHandler

from datetime import date, datetime

from payme.controller.globals import Global

import json
import unittest

from google.appengine.ext import ndb


class UnitTest(unittest.TestCase, PageHandler):
    def __init__(self):
        super(UnitTest, self).__init__('testingPage')
        self.output = ''

     # Get key for the current user
    def getCurrentUser(self):
        return Global.controller.getCurrentUser()

#   MAIN
    def getHTML(self, controller, parameter):

#         CREATE STUFF!! - ONLY RUN ONCE

        currentUser = self.getCurrentUser()

        try:
            john = self.createUser('john', "John Smith")
            david = self.createUser('david', "David Hutchinson")
            dingdong = self.createUser('dingdong', "Ding Dong")
        except:
            john = self.queryUser('john')
            david = self.queryUser('david')
            dingdong = self.queryUser('dingdong')

        group = self.createNewGroup('Wolfpack')

        debt1 = self.createDebt(dingdong.key, john.key, 5000)
        debt2 = self.createDebt(currentUser.key, john.key, 5000)

        self.createPayments(john.key, debt1.key, 300)
        self.createPayments(john.key, debt2.key, 200)

        notification1 = self.createNotification(Notification.Type.INFO, 'Test notification 1')
        notification2 = self.createNotification(Notification.Type.INFO, 'Test notification 2')
        notification3 = self.createNotification(Notification.Type.INFO, 'Test notification 3')

#         ASSOCIATE STUFF!! - ONLY RUN ONCE

#         Add friends
        currentUser.addFriend(john.key)
        currentUser.addFriend(david.key)
        currentUser.addFriend(dingdong.key)

#         Add group
        currentUser.addGroup(group.key)

#         Add member of the group
        group.addMember(john.key)
        group.addMember(dingdong.key)

#           Give John notification
        currentUser.giveNotification(notification1)
        currentUser.giveNotification(notification2)
        david.giveNotification(notification3)

        # Unit Cases
        with self.assertRaises(ValueError):
            # check that OE's are calculated correctly,
            # this also implies that other functions called
            # are correct as getOE called pretty much every other functions
            self.assertEqual(john.getOE(), 4800)
            self.assertEqual(dingdong.getOE(), 4700)

            # check that notifications are sent to correct user,
            self.assertEqual(Notification.query(Notification.key == currentUser.getNotifications()).fetch()[0].getContent(),
                             'Test notification 1')
            # in this case, check that 'Test notification 3' is correctly sent to David
            self.assertEqual(Notification.query(Notification.key == david.getNotifications()).fetch()[0].getContent(),
                             'Test notification 3')

            # check that group is created and associated correctly to the user
            self.assertEqual(group.name, 'Wolfpack')
            self.assertEqual(group.key, currentUser.groups[0])

#   LEAVE THIS ALONE!
        return super(UnitTest, self).getHTML(controller, parameter)


#   HELPER CLASSES

    def queryUser(self, key):
        user = User.query(User.googleID == key).fetch(10)

        if user.__len__() != 0:
            return user[0]
        else:
            return '{error: "User not found"}'

#   Create new single user and returns it
    def createUser(self, userName, name):

        # u = User(id=userName, userName=userName, name=name, dateOfBirth=date(year, mth, day))
        u = User(googleID=userName, name=name, email='user@email.com')
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