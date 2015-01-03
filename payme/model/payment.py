from google.appengine.ext import ndb

class Payment(ndb.Model):
    'A Payment object is used to store the the payment(s) that contribute towards a debt.'

    payer = ndb.KeyProperty(kind='User')
    debt = ndb.KeyProperty(kind='Debt')

    amount = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()

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