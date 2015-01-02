from payme.controller.contentHandler import PageHandler, Parameter

class TransactionsHandler(PageHandler):

    def __init__(self):
        super(TransactionsHandler, self).__init__('transactions')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(TransactionsHandler, self).getHTML(controller, parameter)