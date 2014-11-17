#Imports here
from entity import Entity


class User (Entity):
    'Represents a user in the system'

    def __init__(self, googleID, groups, friends):
        self.googleID = googleID
        self.groups = groups
        self.friends = friends

    def getDebtAmount(self):
        Entity.getDebtAmount(self)

    def getNetAmounts(self):
        Entity.getNetAmounts(self)

    def getNetCreditAmount(self):
        Entity.getNetCreditAmount(self)

    def getCredits(self):
        Entity.getCredits(self)

    def getDebtsAmounts(self):
        Entity.getDebtsAmounts(self)

    def getCreditsAmount(self):
        Entity.getCreditsAmount(self)

    def getDebts(self):
        Entity.getDebts(self)

    def getNetAmount(self):
        Entity.getNetAmount(self)


