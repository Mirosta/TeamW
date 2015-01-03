from payme.model.user import User
from payme.model.debt import Debt
from payme.model.payment import Payment
from payme.model.group import Group
from payme.model.notification import Notification

from datetime import date, datetime

from payme.controller.contentHandler import PageHandler

import json

from google.appengine.ext import ndb


class BuildDB(PageHandler):
    def __init__(self):
        super(BuildDB, self).__init__('testingPage')
        self.output = ''

#   MAIN
    def getHTML(self, controller, parameter):
        self.output += "Starting... <br>"

#         CREATE STUFF!! - ONLY RUN ONCE

        self.output += 'Creating users... <br>'
        john = self.createUser('john', "John Smith")
        david = self.createUser('david', "David Hutchinson")
        dingdong = self.createUser('dingdong', "Ding Dong")

        self.output += 'Creating group, Wolfpack... <br>'
        group = self.createNewGroup('Wolfpack')

        self.output += 'Creating debt (Dingdong to John)... <br>'
        debt = self.createDebt(dingdong.key, john.key, 5000)

        self.output += 'Creating payments... <br>'
        payment = self.createPayments(john.key, debt.key, 300)

        self.output += 'Create notifications... <br><br>'
        notification1 = self.createNotification(Notification.Type.INFO, 'Test notification 1')
        notification2 = self.createNotification(Notification.Type.INFO, 'Test notification 2')
        notification3 = self.createNotification(Notification.Type.INFO, 'Test notification 3')

#         ASSOCIATE STUFF!! - ONLY RUN ONCE

#         Add friends
        self.output += 'Adding David and Dingdong to John... <br>'
        john.addFriend(david.key)
        john.addFriend(dingdong.key)

#         Add group
        self.output += 'Adding Wolpack to John <br>'
        john.addGroup(group.key)

#         Add member of the group
        self.output += 'Adding Dingdong to John\'s Wolfpack...<br>'
        group.addMember(dingdong.key)

#           Give John notification
        self.output += 'Sending John notification...<br>'
        john.giveNotification(notification1.key)
        john.giveNotification(notification2.key)
        david.giveNotification(notification3.key)

        self.output += 'Done... <br>'
        # self.output += "<br>" + self.serialize(group)

#   LEAVE THIS ALONE!
        return super(BuildDB, self).getHTML(controller, parameter)

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
            return obj.strftime('%Y/%m/%d %H:%M:%S')
        elif isinstance(obj, ndb.Key):
            return obj.urlsafe()
        elif isinstance(obj, ndb.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)
