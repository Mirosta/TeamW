from google.appengine.ext import ndb


class Payment(ndb.Model):
    'A Payment object is used to store the the payment(s) that contribute towards a debt.'

    amountPaid = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    description = ndb.StringProperty()

    def getAmountPaid(self):
        return self.amountPaid

    def getDate(self):
        return self.date

    def getDescription(self):
        return self.description