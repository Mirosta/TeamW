from payment import Payment
from google.appengine.ext import ndb
from payme.model.notification import Notification

from payme.controller.globals import Global

import user
from actionable import Actionable

import logging


class Debt(Actionable):
    'Represents a debt that one user owes to another'

    # attributes that are not updatable
    notUpdatableAttributes = ['debtor', 'creditor', 'amount', 'created']

    debtor = ndb.KeyProperty(kind="User")
    creditor = ndb.KeyProperty(kind="User")
    amount = ndb.IntegerProperty()
    description = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    # Able to dispute debt as the creditor
    disputed = ndb.BooleanProperty(default=False)

    def update(self, values):

        super(self.__class__, self).update(values)

        # check if the creator is the debetor
        isIOU = self.getCurrentUser() == self.debtor

        # if 'disputed' update is being updated, send notification to relevant parties
        if 'disputed' in values.keys():
            # if value is being set to true, notify creditor/debtor that the debt has been disputed
            if values['disputed'] is True:
                n = Notification(type=Notification.Type.INFO, content=self.getCurrentUser().name + " has disputed your proposed debt of GBP" + "{0:.2f}".format(self.amount) + " created on " + str(self.created.strftime('%x')) + " .")
            # if the value is being set to false, send creditor/debtor that the dispute has been resolved
            else:
                n = Notification(type=Notification.Type.INFO, content="Your disputed debt of GBP" + "{0:.2f}".format(self.amount) + " with " + self.getCurrentUser().name + " created on " + str(self.created.strftime('%x')) + " has been resolved.")

        # add notification in database entry
        n.put()

        # send notification (and or -- ternary operation to send creditor/debtor)
        user.User.query(user.User.key == (isIOU and self.creditor or self.debtor)).fetch()[0].giveNotification(n)

    # verify that only either debtor or creditor are allowed to create new debt
    def isAddAllowed(self):
        return self.getCurrentUser().key == self.creditor or self.getCurrentUser().key == self.debtor

    # check if the user updating attributes is the creditor, which is the only person who can make changes
    def isUpdateAllowed(self):
        return self.getCurrentUser().key == self.creditor

    def isRemoveAllowed(self):
        return self.isAddAllowed() #TODO decide if this is right

    # Get key for the current user
    def getCurrentUser(self):
        return Global.controller.getCurrentUser()

    # return the original amount of this debt
    def getAmount(self):
        return self.amount

    # return the amount yet to be paid
    def getAmountRemaining(self):
        return self.amount - self.getAmountPaid()

    # return amount paid
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

    # get all payments associated to this debt
    def getPayments(self):
        return Payment.query(Payment.debt == self.key).fetch()

    # notify debtor that new debt has been added to their account
    def notifyDebtor(self):
        debtor = self.queryUser(self.debtor)
        creditor = self.getCurrentUser()

        n = Notification(type=Notification.Type.INFO, content='A debt of ' + Global.formatCurrency(self.amount) + ' has been added to your account by ' + creditor.name)
        n.put()

        debtor.giveNotification(n)

    # notify creditor that new debt has been added to their account
    def notifyCreditor(self):
        debtor = self.queryUser(self.debtor)
        creditor = self.getCurrentUser()

        n = Notification(type=Notification.Type.INFO, content='A credit of ' + Global.formatCurrency(self.amount) + ' has been added to your account by ' + debtor.name)
        n.put()

        creditor.giveNotification(n)

    # this method provides safe remove for debt - this ensures that all dependencies are properly deleted
    def removeMe(self):
        payments = Payment.query(Payment.debt == self.key).fetch()

        for payment in payments:
            payment.key.delete()

        debtor = self.queryUser(self.debtor)
        creditor = self.getCurrentUser()

        n = Notification(type=Notification.Type.INFO, content='Debt of GBP' + Global.formatCurrency(self.amount) + ' has been removed by ' + creditor.name)
        n.put()

        debtor.giveNotification(n)

        self.key.delete()

    # helper function that query user by the key
    def queryUser(self, key):
        return user.User.query(user.User.key == key).fetch()[0]