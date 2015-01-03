from payme.controller.contentHandler import PageHandler


class HelpHandler(PageHandler):

    def __init__(self):
        super(HelpHandler, self).__init__('help')

    def getHTML(self, controller, parameter):
        return super(HelpHandler, self).getHTML(controller, parameter)