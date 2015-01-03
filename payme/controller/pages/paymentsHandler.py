from payme.controller.contentHandler import PageHandler, Parameter
from payme.controller.modelHandler import ModelHandler
from payme.model.payment import Payment


class PaymentsHandler(ModelHandler):

    def __init__(self):
        super(PaymentsHandler, self).__init__('payments', {}, 'getAllPayments', Payment, [], [])
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(PaymentsHandler, self).getHTML(controller, parameter)