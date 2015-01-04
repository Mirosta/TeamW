from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.controller.modelHandler import ModelHandler, ReadOnlyFunction
from payme.model.payment import Payment


class PaymentsHandler(ModelHandler):

    def __init__(self):
        super(PaymentsHandler, self).__init__('payments', {'add' : PaymentsHandler.AddHandler()}, 'getAllPayments', Payment, [], [ReadOnlyFunction("getPayee", "payee")])
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    class AddHandler(VerbHandler):
        def __init__(self):
            super(PaymentsHandler.AddHandler, self).__init__('addPayment')
            self.parameter = Parameter(Parameter.Type.NoParameter, False, False)
