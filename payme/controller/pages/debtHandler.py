from payme.controller import validator
from payme.controller.contentHandler import PageHandler, Parameter, VerbHandler
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction, ModelAddHandler, \
    ModelRemoveHandler, ModelUpdateHandler
from payme.model.debt import Debt
from payme.model.user import User
from payme.model.payment import Payment

class DebtHandler(ModelHandler):

    def __init__(self):
        super(DebtHandler, self).__init__(None,
                                          {'add': AddHandler('addDebt'),
                                           'pay': PayHandler(),
                                           'remove': RemoveHandler(),
                                           'update': ModelUpdateHandler()},
                                          'getAllRelatedDebts',
                                          Debt,
                                          [RelatedModel(Payment, 'debt', 'payments')],
                                          [ReadOnlyFunction('getStatus', 'status'),
                                           ReadOnlyFunction('getAmountPaid', 'amountPaid'),
                                           ReadOnlyFunction('getAmountRemaining', 'amountRemaining')])

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
        return User.query(User.googleID == googleID).fetch()[0]

    def onInvalidParameter(self):
        return '{error: "Invalid debt key"}'

    # Not sure about this...
    # def onUnknownFriend(self):
    #     return '{error: "No friend with that ID"}'


class AddHandler(ModelAddHandler):

    def postAPI(self, controller, parameter, postData):
        try:
            debt = validator.create(postData, self.type)
            # add new entity to database
            debt.put()
            #debt.notifyDebtor()
            return '{"success": 1}'
        except Exception as e:
            raise e


class RemoveHandler(ModelRemoveHandler):

    def __init__(self):
        super(RemoveHandler, self).__init__('remove')

    def postAPI(self, controller, parameter, postData):
        try:
            debt = validator.retrieve(postData, self.type)
            # remove entity from database
            debt.removeMe()
            return '{"success": 1}'
        except Exception as e:
            raise e


class PayHandler(VerbHandler):

    def __init__(self):
        super(PayHandler, self).__init__('pay')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(PayHandler, self).getHTML(controller, parameter)