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

    payer = ndb.KeyProperty(kind='User')
    debt = ndb.KeyProperty(kind='Debt')

    amount = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()

    # # the debtor of the debt
    # approvedByDebtor = ndb.BooleanProperty(default=False)

    # the creditor of the debt i.e. the Payer
    approvedByCreditor = ndb.BooleanProperty(default=False)

    # the creditor of the debt can dispute an individual payment (payment has to be made to be disputed)
    disputed = ndb.BooleanProperty(default=False)

    def isAddAllowed(self):
        return self.getCurrentUser().key == self.payer and self.queryDebt(self.debt).getAmount() - (self.queryDebt(self.debt).getAmountPaid() + self.amount) >= 0

    def queryDebt(self, debtKey):
        return debt.Debt.query(debt.Debt.key == debtKey).fetch()[0]

    def isUpdateAllowed(self):
        logging.info("Checking that current user is the creditor for this payment")
        logging.info(str(self.getCurrentUser()))
        return self.getCurrentUser().key == self.getDebt().creditor

    def isRemoveAllowed(self):
        return self.isUpdateAllowed()

    def update(self, values):

        super(self.__class__, self).update(values)

        if 'disputed' in values.keys():
            if values['disputed'] is True:
                n = Notification(type=Notification.Type.INFO, content=self.getCurrentUser().name + " has disputed your payment of " + Global.formatCurrency(self.amount) + " made on " + str(self.created.strftime('%x')) + " .")

            else:
                n = Notification(type=Notification.Type.INFO, content="Your disputed payment of GBP" + Global.formatCurrency(self.amount) + " with " + self.getCurrentUser().name + " made on " + str(self.created.strftime('%x')) + " has been resolved.")

            n.put()
            user.User.query(user.User.key == self.payer).fetch()[0].giveNotification(n)

        if 'approvedByCreditor' in values.keys():
            n = Notification(type=Notification.Type.INFO, content=self.getCurrentUser().name + " has accepted your payment of " + Global.formatCurrency(self.amount) + " made on " + str(self.created.strftime('%x')) + " .")
            n.put()

            user.User.query(user.User.key == self.payer).fetch()[0].giveNotification(n)

    # Get key for the current user
    def getCurrentUser(self):
        return Global.controller.getCurrentUser()

    def getPayer(self):
        return user.User.query(user.User.key == self.payer)

    def getDebt(self):
        return debt.Debt.query(debt.Debt.key == self.debt).fetch()[0]

    def getPayee(self):
        return self.getDebt().debtor

    def getAmount(self):
        return self.amount

    def getDate(self):
        return self.date

    def getDescription(self):
        return self.description

    def raiseDispute(self):

        if self.getDebt().getCreditor() != self.getCurrentUser().key:
            raise SecurityError()

        self.disputed = True
        self.put()



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


