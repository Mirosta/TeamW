#Imports here
from entity import Entity


class User (Entity):
    'Represents a user in the system'

    def __init__(self, googleID, groups, friends):
        self.googleID = googleID
        self.groups = groups
        self.friends = friends

    def getDebtAmount(self):
        pass

    def getNetAmounts(self):
        pass

    def getNetCreditAmount(self):
        pass

    def getCredits(self):
        pass

    def getDebtsAmounts(self):
        pass

    def getCreditsAmount(self):
        pass

    def getDebts(self):
        pass

    def getNetAmount(self):
        pass
