from payme.controller.contentHandler import PageHandler, Parameter, VerbHandler
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction
from payme.model.debt import Debt
from payme.model.user import User
from payme.model.payment import Payment

class DebtHandler(ModelHandler):

    # dummy for currentUser
    #currentUser = User.query(User.googleID == 'john').fetch(10)[0]

    def __init__(self):
        super(DebtHandler, self).__init__(None,
                                          {'add': AddHandler(), 'pay': PayHandler()},
                                          'getCRs',
                                          Debt,
                                          [RelatedModel(Payment, 'debt', 'payments'),
                                           ReadOnlyFunction('getStatus', 'status')])

    # returns all debt owed by that user - CHECKED
    def displayAllDebt(self):

        debts = self.currentUser.getCRs()
        debtsOutput = []

        for debt in debts:
            data = debt.to_dict()

            payments = Payment.query(Payment.debt == debt.key)
            paymentOutput = []

            for payment in payments:
                paymentOutput.append(payment.key)

            data['readOnly'] = {'payments': paymentOutput}

            debtsOutput.append(data)

        return self.serialize({'results': debtsOutput})

    # returns all debt owed by that user to a specified creditor - CHECKED
    def displayDebtOweTo(self, key):
        return self.serialize(Debt.query(Debt.debtor == self.currentUser.key, Debt.creditor == self.queryUserByID(key).key).fetch(10))

    # debug - helper for function above
    def queryUserByID(self, googleID):
        return User.query(User.googleID == googleID).fetch(10)[0]

    def onInvalidParameter(self):
        return '{error: "Invalid debt key"}'

    # Not sure about this...
    # def onUnknownFriend(self):
    #     return '{error: "No friend with that ID"}'


class AddHandler(VerbHandler):

    def __init__(self):
        super(AddHandler, self).__init__('add')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(AddHandler, self).getHTML(controller, parameter)

class PayHandler(VerbHandler):

    def __init__(self):
        super(PayHandler, self).__init__('pay')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(PayHandler, self).getHTML(controller, parameter)