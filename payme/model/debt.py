from payment import Payment
from google.appengine.ext import ndb
from payme.model.notification import Notification

from payme.controller.globals import Global

import user

import logging


class Debt(ndb.Model):
    'Represents a debt that one user owes to another'

    debtor = ndb.KeyProperty(kind="User")
    creditor = ndb.KeyProperty(kind="User")
    amount = ndb.IntegerProperty()
    description = ndb.StringProperty()
    isPaid = ndb.BooleanProperty()
    date = ndb.DateTimeProperty()
    dateCreated = ndb.DateTimeProperty(auto_now_add=True)
    amountPaid = ndb.IntegerProperty()

    # Able to dispute debt as the creditor
    disputed = ndb.BooleanProperty(default=False)

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

    def removeMe(self):
        payments = Payment.query(Payment.debt == self.key).fetch()

        for payment in payments:
            payment.key.delete()

        debtor = user.User.query(user.User.key == self.debtor).fetch()[0]
        creditor = self.getCurrentUser()

        # TODO implement real user thingy
        # n = Notification(type=Notification.Type.INFO, content='Debt of GBP' + "{0:.2f}".format(self.amount) + ' has been removed by ' + creditor.name)
        n = Notification(type=Notification.Type.INFO, content='Debt of GBP' + "{0:.2f}".format(self.amount) + ' has been removed by ' + str(creditor.googleID))
        n.put()

        debtor.giveNotification(n)

        self.key.delete()
