

from payme.controller.contentHandler import PageHandler

class TestPage(PageHandler):

    def __init__(self):
        super(TestPage, self).__init__('testingPage')
        self.output = ''

    def getHTML(self, controller, parameter):
        self.output = 'Hello World'
        return super(TestPage, self).getHTML(parameter)