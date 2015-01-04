from payme.controller.contentHandler import PageHandler, Parameter
from payme.controller.contentHandler import VerbHandler
from payme.controller.modelHandler import ModelHandler
from payme.model.payment import Payment


class PaymentsHandler(ModelHandler):

    def __init__(self):
        super(PaymentsHandler, self).__init__('payments', {'add' : PaymentsHandler.AddHandler()}, 'getAllPayments', Payment, [], [ReadOnlyFunction("getPayee", "payee")])
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    class AddHandler(VerbHandler):
        def __init__(self):
            super(PaymentsHandler.AddHandler, self).__init__('addPayment')
            self.parameter = Parameter(Parameter.Type.NoParameter, False, False)
