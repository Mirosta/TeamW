from google.appengine.ext import ndb

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

    # the debtor of the debt can dispute an individual payment (payment has to be made to be disputed)
    disputed = ndb.BooleanProperty(default=False)

    def getPayer(self):
        return self.payer

    def getDebt(self):
        return self.debt

    def getAmount(self):
        return self.amount

    def getDate(self):
        return self.date

    def getDescription(self):
        return self.description

    # unpaid = none, inProgress = one approved,
    # paid = both approved, inDispute = disputed
    def getStatus(self):

        # see if its disputed first
        if self.disputed:
            return "INDISPUTE"

        # otherwise work out the progress of the payments
        if self.approvedByCreditor:
            if self.approvedByDebtor:
                return "PAID"
            else:
                return "INPROGRESS"
        else:
            return "UNPAID"






