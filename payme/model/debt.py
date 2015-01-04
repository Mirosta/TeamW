from payment import Payment
from google.appengine.ext import ndb
from payme.model.notification import Notification

from payme.controller.globals import Global

import user
from actionable import Actionable

import logging


class Debt(Actionable):
    'Represents a debt that one user owes to another'

    notUpdatableAttributes = ['debtor', 'creditor', 'amount', 'created']

    debtor = ndb.KeyProperty(kind="User")
    creditor = ndb.KeyProperty(kind="User")
    amount = ndb.IntegerProperty()
    description = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    # Able to dispute debt as the debtor
    disputed = ndb.BooleanProperty(default=False)

    def update(self, values):

        super(self.__class__, self).update(values)

        isIOU = self.getCurrentUser() == self.debtor

        logging.info(str(values.keys()))

        if 'disputed' in values.keys():
            logging.info('in disputed')
            if values['disputed'] is True:
                logging.info('creating notification....')
                n = Notification(type=Notification.Type.INFO, content=self.getCurrentUser().name + " has disputed your proposed debt of GBP" + "{0:.2f}".format(self.amount) + " created on " + str(self.created.strftime('%x')) + " .")
            else:
                n = Notification(type=Notification.Type.INFO, content="Your disputed debt of GBP" + "{0:.2f}".format(self.amount) + " with " + self.getCurrentUser().name + " created on " + str(self.created.strftime('%x')) + " has been resolved.")

        n.put()
        user.User.query(user.User.key == (isIOU and self.creditor or self.debtor)).fetch()[0].giveNotification(n)

    def isAddAllowed(self):
        return self.getCurrentUser().key == self.creditor or self.getCurrentUser().key == self.debtor

    def isUpdateAllowed(self):
        return self.getCurrentUser().key == self.creditor

    def isRemoveAllowed(self):
        return self.isAddAllowed()

    # Get key for the current user
    def getCurrentUser(self):
        return Global.controller.getCurrentUser()

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

        amountPaid = self.getAmountPaid()

        # otherwise work out the progress of the payments
        if amountPaid > 0:
            if amountPaid >= self.amount:
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

        n = Notification(type=Notification.Type.INFO, content='A debt of ' + Global.formatCurrency(self.amount) + ' has been added to your account by ' + creditor.name)
        n.put()

        debtor.giveNotification(n)

    def removeMe(self):
        payments = Payment.query(Payment.debt == self.key).fetch()

        for payment in payments:
            payment.key.delete()

        debtor = self.queryUser(self.debtor)
        creditor = self.getCurrentUser()

        # TODO implement real user thingy
        # n = Notification(type=Notification.Type.INFO, content='Debt of GBP' + "{0:.2f}".format(self.amount) + ' has been removed by ' + creditor.name)
        n = Notification(type=Notification.Type.INFO, content='Debt of ' + Global.formatCurrency(self.amount) + ' has been removed by ' + creditor.googleID)
        n.put()

        debtor.giveNotification(n)

        self.key.delete()

    def queryUser(self, key):
        return user.User.query(user.User.key == key).fetch()[0]