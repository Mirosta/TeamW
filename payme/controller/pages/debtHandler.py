from payme.controller.contentHandler import PageHandler, Parameter, VerbHandler

class DebtHandler(PageHandler):

    def __init__(self):
        super(DebtHandler, self).__init__(None, Parameter(), {'add': AddHandler(), 'pay': PayHandler()})

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