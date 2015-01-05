from google.appengine.ext import ndb
from payme.model.notification import Notification
from payme.controller.exceptions import SecurityError
from actionable import Actionable
import debt
import logging

from payme.controller.globals import Global

import user

class Payment(Actionable):
    'A Payment object is used to store the the payment(s) that contribute towards a debt.'

    notUpdatableAttributes = ['payer', 'debt', 'created', 'amount']

    # The user who is paying the payment and the user who is to received the payment.
    payer = ndb.KeyProperty(kind='User')
    debt = ndb.KeyProperty(kind='Debt')

    # An amount and description is added by the application user
    amount = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()

    # # the debtor of the debt
    # approvedByDebtor = ndb.BooleanProperty(default=False)

    # the creditor of the debt i.e. the Payer
    approvedByCreditor = ndb.BooleanProperty(default=False)

    # the creditor of the debt can dispute an individual payment (payment has to be made to be disputed)
    disputed = ndb.BooleanProperty(default=False)

    # Override to check if adding a new payment is allowed, i.e. you are the payer
    # and you are not about to overpay the debt
    def isAddAllowed(self):
        return self.getCurrentUser().key == self.payer and self.queryDebt(self.debt).getAmount() - (self.queryDebt(self.debt).getAmountPaid() + self.amount) >= 0

    # Utility method to obtain the debt associated with this payment for further checks
    def queryDebt(self, debtKey):
        return debt.Debt.query(debt.Debt.key == debtKey).fetch()[0]

    # Override to check if the current user can update a payment.
    # They must be the creditor (the one getting the money) of the debt
    # associated with this payment.
    def isUpdateAllowed(self):
        return self.getCurrentUser().key == self.getDebt().creditor

    def isRemoveAllowed(self):
        return self.isUpdateAllowed()

    def queryUser(self, key):
        return user.User.query(user.User.key == key).fetch()[0]

    def notifyCreditor(self):
        payerObj = self.getPayer()

        n = Notification(type=Notification.Type.INFO, content=payerObj.name + " has made a payment of " + Global.formatCurrency(self.amount) + " to you on " + str(self.created.strftime('%x')) + ".")

        n.put()

        self.queryUser(self.getDebt().creditor).giveNotification(n)

    # An overridden version of Actionable's update()
    # This super call is made and notifications are made depending on whether
    # the payment has just been disputed and/or approved.
    def update(self, values):

        super(self.__class__, self).update(values)

        if 'disputed' in values.keys():
            if values['disputed'] is True:
                n = Notification(type=Notification.Type.INFO, content=self.getCurrentUser().name + " has disputed your payment of " + Global.formatCurrency(self.amount) + " made on " + str(self.created.strftime('%x')) + " .")

            else:
                n = Notification(type=Notification.Type.INFO, content="Your disputed payment of GBP" + Global.formatCurrency(self.amount) + " with " + self.getCurrentUser().name + " made on " + str(self.created.strftime('%x')) + " has been resolved.")

            n.put()

            self.queryUser(self.payer).giveNotification(n)

        if 'approvedByCreditor' in values.keys():
            n = Notification(type=Notification.Type.INFO, content=self.getCurrentUser().name + " has accepted your payment of " + Global.formatCurrency(self.amount) + " made on " + str(self.created.strftime('%x')) + " .")
            n.put()

            self.queryUser(self.payer).giveNotification(n)


    # Get key for the current user
    def getCurrentUser(self):
        return Global.controller.getCurrentUser()

    # Getters
    def getPayer(self):
        return user.User.query(user.User.key == self.payer)

    def getDebt(self):
        return debt.Debt.query(debt.Debt.key == self.debt).fetch()[0]

    def getPayee(self):
        return self.getDebt().creditor

    def getAmount(self):
        return self.amount

    def getDate(self):
        return self.date

    def getDescription(self):
        return self.description

    # Method to raise a dispute if necessary in the backend
    def raiseDispute(self):

        if self.getDebt().getCreditor() != self.getCurrentUser().key:
            raise SecurityError()

        self.disputed = True
        self.put()

    # A method to compute the current status of the payment.
    # Obtained in the JSON from the readOnly values.
    # approved = creditor approves, awaiting_approval = not approved,
    # in_dispute = disputed
    def getStatus(self):

        # see if its disputed first
        if self.disputed:
            return 'IN_DISPUTE'

        # otherwise work out the progress of the payment
        if self.approvedByCreditor:
            return 'APPROVED'
        else:
            return 'AWAITING_APPROVAL'


