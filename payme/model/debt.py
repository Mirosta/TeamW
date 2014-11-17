from user import User
from payment import Payment

class Debt:
    'Represents a debt that one user owes to another'

    def __init__(self, debtor, creditor, amount, amountsPaid, description, isPaid, date, dateCreated, amountPaid):
        self.debtor = debtor
        self.creditor = creditor
        self.amount = amount
        self.amountsPaid = amountsPaid
        self.description = description
        self.isPaid = isPaid
        self.date = date
        self.dateCreated = dateCreated
        self.amountPaid = amountPaid

    def getAmountRemaining(self):
        pass
