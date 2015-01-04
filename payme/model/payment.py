from google.appengine.ext import ndb
from payme.model.notification import Notification
from payme.controller.exceptions import SecurityError
import debt

from payme.controller.globals import Global

import user

class Payment(ndb.Model):
    'A Payment object is used to store the the payment(s) that contribute towards a debt.'

    payer = ndb.KeyProperty(kind='User')
    debt = ndb.KeyProperty(kind='Debt')

    amount = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()

    # the debtor of the debt
    approvedByDebtor = ndb.BooleanProperty(default=False)

    # the creditor of the debt i.e. the Payer
    approvedByCreditor = ndb.BooleanProperty(default=False)

    # the creditor of the debt can dispute an individual payment (payment has to be made to be disputed)
    disputed = ndb.BooleanProperty(default=False)

    # Get key for the current user
    def getCurrentUser(self):
        #TODO return Global.apiController.getCurrentUser()
        return user.User.query(user.User.googleID == 'john').fetch()[0]

    def getPayer(self):
        return user.User.query(user.User.key == self.payer)

    def getDebt(self):
        return debt.Debt.query(debt.Debt.key == self.debt).fetch()[0]

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

        n = Notification(type=Notification.Type.INFO, content=" Your payment of GBP" + "{0:.2f}".format(self.amount) + " made on " + str(self.date.strftime('%x')) + " has been disputed.")
        n.put()

        user.User.query(user.User.key == self.payer).fetch()[0].giveNotification(n)

    # unpaid = none, inProgress = one approved,
    # paid = both approved, inDispute = disputed
    def getStatus(self):

        # see if its disputed first
        if self.disputed:
            return 'INDISPUTE'

        # otherwise work out the progress of the payments
        if self.approvedByCreditor:
            if self.approvedByDebtor:
                return 'PAID'
            else:
                return 'INPROGRESS'
        else:
            return 'UNPAID'

