from payment import Payment
from google.appengine.ext import ndb
from payme.model.notification import Notification

from payme.controller.globals import Global

import user
from actionable import Actionable

import logging


class Debt(Actionable):
    'Represents a debt that one user owes to another'

    debtor = ndb.KeyProperty(kind="User")
    creditor = ndb.KeyProperty(kind="User")
    amount = ndb.IntegerProperty()
    description = ndb.StringProperty()
    isPaid = ndb.BooleanProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    amountPaid = ndb.IntegerProperty()

    # Able to dispute debt as the debtor
    disputed = ndb.BooleanProperty(default=False)

    def isAddAllowed(self):
        return self.getCurrentUser().key == self.creditor or self.getCurrentUser().key == self.debtor

    def isUpdateAllowed(self):
        return self.getCurrentUser().key == self.creditor

    # Get key for the current user
    def getCurrentUser(self):
        #TODO return Global.apiController.getCurrentUser()
        return user.User.query(user.User.googleID == 'john').fetch()[0]

    def getAmount(self):
        return self.amount

    def getAmountRemaining(self):
        return self.amount - self.getAmountPaid()

    def getAmountPaid(self):
        payments = Payment.query(Payment.debt == self.key).fetch()

        totalPaid = 0

        for payment in payments:
            totalPaid += payment.getAmount()

        return totalPaid

    # unpaid = none, inProgress = 0 < amountPaid < amount,
    # paid - amountPaid = amount, inDispute = disputed
    def getStatus(self):

        # see if its disputed first
        if self.disputed:
            return "INDISPUTE"

        # otherwise work out the progress of the payments
        if self.amountPaid > 0:
            if self.amountPaid == self.amount:
                return "PAID"
            else:
                return "INPROGRESS"
        else:
            return "UNPAID"

    def getPayments(self):
        return Payment.query(Payment.debt == self.key).fetch()

    def notifyDebtor(self):
        debtor = self.queryUser(self.debtor)
        creditor = self.getCurrentUser()

        n = Notification(type=Notification.Type.INFO, content='A debt of GBP' + "{0:.2f}".format(self.amount) + ' has been added to your account by ' + creditor.name)
        n.put()

        debtor.giveNotification(n)

    def removeMe(self):
        payments = Payment.query(Payment.debt == self.key).fetch()

        for payment in payments:
            payment.key.delete()

        debtor = self.queryUser(self.debtor)
        creditor = self.getCurrentUser()

        n = Notification(type=Notification.Type.INFO, content='Debt of GBP' + "{0:.2f}".format(self.amount) + ' has been removed by ' + creditor.name)
        n.put()

        debtor.giveNotification(n)

        self.key.delete()

    def queryUser(self, key):
        return user.User.query(user.User.key == key).fetch()[0]