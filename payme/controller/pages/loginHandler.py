from payme.controller.contentHandler import ContentHandler, Parameter


class LoginHandler(ContentHandler):

    def __init__(self):
        super(LoginHandler, self).__init__('login')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(LoginHandler, self).getHTML(controller, parameter)