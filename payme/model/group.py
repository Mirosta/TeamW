from google.appengine.ext import ndb

from entity import Entity
from debt import Debt

# Group is made by passing a list of users. When addDebt is called, it will add 'debt' passed to every user in the group.
class Group (Entity):

    users = ndb.KeyProperty(kind='User', repeated=True)

    def addUser(self, user):
        self.users.append(user)

    def renameGroup(self, name):
        self.name = name

    #TODO: Do some division on the amount of debt to add
    # When debt is evenly distributed to everyone in the group
    def addDebtEven(self, debt):

        amountTotal = debt.getAmountRemaining()
        amountEach = amountTotal / self.users.__len__()

        # create debts and put them in database
        for user in self.users:
            d = Debt(debtor=user,
                     creditor=debt.creditor,
                     amount=amountEach,
                     description=debt.description,
                     isPaid=False,
                     date=debt.date)

            d.put()

    # When debt is not applied to the entire group
    # Split evenly among users provided
    def addDebtUneven(self, debt, users):

        amountTotal = debt.getAmountRemaining();
        amountEach = amountTotal / users.__len__()

        # create debts and put then in database
        for user in self.users:
            d = Debt(debtor=user,
                     creditor=debt.creditor,
                     amount=amountEach,
                     description=debt.description,
                     isPaid=False,
                     date=debt.date)

            d.put()


    #TODO: Implement methods
    def getDebtAmount(self):
        return super(Group, self).getDebtAmount()

    def getNetAmounts(self):
        return super(Group, self).getNetAmounts()

    def getNetCreditAmount(self):
        return super(Group, self).getNetCreditAmount()

    def getCredits(self):
        return super(Group, self).getCredits()

    def getDebtsAmounts(self):
        return super(Group, self).getDebtsAmounts()

    def getCreditsAmount(self):
        return super(Group, self).getCreditsAmount()

    def getDebts(self):
        super(Group, self).getDebts()

    def getNetAmount(self):
        return super(Group, self).getNetAmount()


