from google.appengine.ext import ndb


class Entity(ndb.model):

    def __init__(self, name):
        self.name = name

    def getDebts(self):
        """
        :rtype: dict of {User: Debt[]}
        :return:
        """
        pass

    def getCredits(self):
        raise NotImplementedError('The subclass has forgotten to implement this method')

    def getDebtsAmounts(self):
        raise NotImplementedError('The subclass has forgotten to implement this method')

    def getCreditsAmount(self):
        raise NotImplementedError('The subclass has forgotten to implement this method')

    def getNetAmounts(self):
        raise NotImplementedError('The subclass has forgotten to implement this method')

    def getDebtAmount(self):
        raise NotImplementedError('The subclass has forgotten to implement this method')

    def getNetCreditAmount(self):
        raise NotImplementedError('The subclass has forgotten to implement this method')

    def getNetAmount(self):
        raise NotImplementedError('The subclass has forgotten to implement this method')