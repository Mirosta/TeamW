from google.appengine.ext import ndb

from entity import Entity
from debt import Debt

from payme.controller.exceptions import OwnerInGroupError

import user

import logging

from payme.controller.globals import Global

# Group is made by passing a list of users. When addDebt is called, it will add 'debt' passed to every user in the group.
class Group (Entity):

    users = ndb.KeyProperty(kind='User', repeated=True)

    # Get key for the current user
    def getCurrentUser(self):
        # return Global.apiController.getCurrentUser().key
        return user.User.query(user.User.googleID == 'john').fetch()[0].key

    def addMember(self, user):
        if self.getCurrentUser() == user:
            raise OwnerInGroupError
        else:
            self.users.append(user)
            self.put()

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

        output = 0

        for u in self.users:
            output += user.User.query(user.User.key == u).fetch()[0].getDR();

        return output

        # return super(Group, self).getDebtAmount()

    def getCreditAmount(self):

        output = 0

        logging.info('!!!!!!!!!!!!!!!!!!!!' + str(self.users.__len__()))

        for u in self.users:

            output += user.User.query(user.User.key == u).fetch()[0].getCR()

        return output

        # return super(Group, self).getNetCreditAmount()

    def getNetAmounts(self):

        output = []

        for u in self.users:
            netAmount = u.getCR - u.getDR
            output.append({u: netAmount})

        return output

        # return super(Group, self).getNetAmounts()

    def getCredits(self):

        output = []

        for u in self.users:
            output.append(u.getCredits())

        return output

    def getDebts(self):

        output = []

        for u in self.users:
            output.append(u.getDebt())

        return output

    def getDebtsAmounts(self):

        output = []

        for u in self.users:
            output.append(u.getDebtAmounts)

        return output

        # return super(Group, self).getDebtsAmounts()

    def getCreditsAmount(self):

        output = []

        for u in self.users:
            output.append(u.getCreditAmounts)

        return output

        # return super(Group, self).getCreditsAmount()

    def getNetAmount(self):
        return self.getCreditAmount() - self.getDebtAmount()

        # return super(Group, self).getNetAmount()

    def queryDebts(self):
        return Debt.query(Debt.debtor == self.currentUser.key)

    def removeMe(self):
        self.getCurrentUser().removeGroup(self.key)
        self.key.delete()