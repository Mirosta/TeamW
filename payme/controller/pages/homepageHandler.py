from payme.controller.contentHandler import PageHandler, Parameter

# Test page with a test template
class HomepageHandler(PageHandler):

    def __init__(self):
        super(HomepageHandler, self).__init__('home')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(HomepageHandler, self).getHTML(controller, parameter)