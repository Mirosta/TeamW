#Imports here
from entity import Entity
from group import Group
import debt

from google.appengine.ext import ndb

class User (Entity):
    # Database for users

    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()

    googleID = ndb.StringProperty()
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    groups = ndb.StructuredProperty(Group, repeated=True)
    friends = ndb.KeyProperty(kind='User', repeated=True)
    dateOfBirth = ndb.DateProperty()
    credentials = ndb.PickleProperty() #Store the OAuthCredentials

    uniqueProperty = 'googleID'

    # Get list of assets
    def getDRs(self):
        return debt.Debt.query(debt.Debt.creditor == self.key).fetch()

    # Get list of liabilities
    def getCRs(self):
        return debt.Debt.query(debt.Debt.debtor == self.key).fetch()

    # Get assets amount
    def getDR(self):
        debits = self.getDRs()

        totalDR = 0

        for debit in debits:
            totalDR != debit.getAmountRemaining()

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