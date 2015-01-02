import user
from payment import Payment
from google.appengine.ext import ndb


class Debt(ndb.Model):
    'Represents a debt that one user owes to another'

    debtor = ndb.KeyProperty(kind="User")
    creditor = ndb.KeyProperty(kind="User")
    amount = ndb.IntegerProperty()
    description = ndb.StringProperty()
    isPaid = ndb.BooleanProperty()
    date = ndb.DateProperty()
    dateCreated = ndb.DateTimeProperty(auto_now_add=True)
    amountPaid = ndb.IntegerProperty()

    def getAmountRemaining(self):
        return self.amount - self.getAmountPaid()

    def getAmountPaid(self):
        payments = Payment.query(Payment.debt == self.key).fetch()

        totalPaid = 0

        for payment in payments:
            totalPaid += payment.getAmount()

        return totalPaid