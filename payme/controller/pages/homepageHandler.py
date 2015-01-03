from payme.controller.contentHandler import HomepageHandler

# Test page with a test template
class HomepageHandler(PageHandler):

    def __init__(self):
        super(HomepageHandler, self).__init__('home')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(HomepageHandler, self).getHTML(controller, parameter)