#Imports here
from entity import Entity
from group import Group
from payme.model.debt import Debt
from payme.controller.exceptions import SecurityError

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

    # Get key for the current user
    def getCurrentUser(self):
        # return Global.apiController.getCurrentUser().key
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

    # debug
    def retrieveUserName(self):
        return self.googleID