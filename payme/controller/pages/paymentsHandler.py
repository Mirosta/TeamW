from payme.controller.contentHandler import PageHandler, Parameter

class PaymentsHandler(PageHandler):

    def __init__(self):
        super(PaymentsHandler, self).__init__('payments')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(PaymentsHandler, self).getHTML(controller, parameter)