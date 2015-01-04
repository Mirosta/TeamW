from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.controller.modelHandler import ModelHandler, ReadOnlyFunction, ModelAddHandler
from payme.model.payment import Payment


class PaymentsHandler(ModelHandler):

    def __init__(self):
        super(PaymentsHandler, self).__init__('payments', {'add' : ModelAddHandler('addPayment')}, 'getAllPayments', Payment, [], [ReadOnlyFunction("getPayee", "payee")])
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)