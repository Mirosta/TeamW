from entity import Entity
from group import Group
from notification import Notification
import debt
from payme.model.debt import Debt
from payme.controller.exceptions import SecurityError
from payme.model.notification import Notification

from payme.controller.globals import Global

from google.appengine.ext import ndb

class User (Entity):
    # Database for users

    googleID = ndb.StringProperty()
    familyName = ndb.StringProperty()
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    groups = ndb.KeyProperty(kind=Group, repeated=True)
    friends = ndb.KeyProperty(kind='User', repeated=True)
    profilePicture = ndb.StringProperty()
    credentials = ndb.PickleProperty() # Store the OAuthCredentials

    uniqueProperty = 'googleID'

    # notification queue
    messageQueue = ndb.KeyProperty(kind=Notification, repeated=True)

    # Hacky way to return user for model
    def getMe(self):
        return [self]

    # Get key for the current user
    def getCurrentUser(self):
        #TODO return Global.apiController.getCurrentUser().key
        return User.query(User.googleID == 'john').fetch()[0].key

    def isMe(self):
        return self.getCurrentUser() == self.key

    # Get list of assets
    def getDRs(self):
        if self.isMe():
            return Debt.query(Debt.creditor == self.key).fetch()
        else:
            return Debt.query(Debt.creditor == self.key, Debt.debtor == self.getCurrentUser()).fetch()

    # Get list of liabilities
    def getCRs(self):
        if self.isMe():
            return Debt.query(Debt.debtor == self.key).fetch()
        else:
            return Debt.query(Debt.debtor == self.key, Debt.creditor == self.getCurrentUser()).fetch()

    # Get assets amount
    def getDR(self):
        debits = self.getDRs()

        totalDR = 0

        for debit in debits:
            totalDR += debit.getAmountRemaining()

        return totalDR

    # Get liabilities amount
    def getCR(self):
        credits = self.getCRs()

        totalCR = 0

        for credit in credits:
            totalCR += credit.getAmountRemaining()

        return totalCR

    # Get owner equities
    def getOE(self):
        return self.getDR() - self.getCR()

    # create new group
    def addGroup(self, group):
        if self.isMe and group not in self.groups:
            self.groups.append(group)
            self.put()
        else:
            raise SecurityError()


    def getFriends(self):
        if self.isMe() or self.getCurrentUser() in self.friends:
            output = []
            for friend in self.friends:
                output.append(User.query(User.key == friend).fetch()[0])
            return output
        else:
            raise SecurityError()

    def getGroups(self):
        if self.isMe():
            output = []
            for group in self.groups:
                output.append(Group.query(Group.key == group).fetch()[0])
            return output
        else:
            raise SecurityError()

    # add friend
    def addFriend(self, friend):
        if self.isMe():
            self.friends.append(friend)
            self.put()

            n = Notification(type=Notification.Type.FRIEND_REQUEST,
                             content=str(self.name) + ' tried to add you as a friend.')
            n.put()

            friend.giveNotification(n)
        else:
            raise SecurityError()

    def getDebts(self):
        return {self : self.getCRs()}

    def getCredits(self):
        return {self : self.getDRs()}

    def getDebtAmounts(self):
        debtAmounts = []
        debts = self.getCRs()

        for debt in debts:
            debtAmounts.append(debt.getAmountRemaining())

        return {self : debtAmounts}

    def getCreditAmounts(self):
        creditAmounts = []
        credits = self.getDRs()

        for credit in credits:
            creditAmounts.append(credit.getAmountRemaining())

        return {self : creditAmounts}

    # add a notification to the user's message queue
    def giveNotification(self, notificationObj):
        self.messageQueue.append(notificationObj.key)
        self.put()

    # retrieve a notification from the message queue (if present)
    def getNotifications(self):

        output = []

        for notification in self.messageQueue:
            output.append(Notification.query(Notification.key == notification).fetch()[0])

        return output

    def getAllPayments(self):
        debts = self.getDRs()
        credits = self.getCRs()

        payments = []

        for debt in debts:
            payments.extend(debt.getPayments())

        for credit in credits:
            payments.extend(credit.getPayments())

        return payments

    def removeGroup(self, group):
        if group.key in self.groups:
            self.groups.remove(group.key)
        self.put()

    # debug
    def retrieveUserName(self):
        return self.googleID