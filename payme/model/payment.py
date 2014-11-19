from google.appengine.ext import ndb


class Payment(ndb.Model):
    'A Payment object is used to store the the payment(s) that contribute towards a debt.'

    def __init__(self, amountPaid, date, description):
        self.amountPaid = amountPaid
        self.date = date
        self.description = description

    def getAmountPaid(self):
        return self.amountPaid

    def getDate(self):
        return self.date

    def getDescription(self):
        return self.description