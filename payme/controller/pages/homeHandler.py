from payme.controller.contentHandler import PageHandler, Parameter

class HomeHandler(PageHandler):

    def __init__(self):
        super(HomeHandler, self).__init__('home')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(HomeHandler, self).getHTML(controller, parameter)