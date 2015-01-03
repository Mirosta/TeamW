from payme.controller.contentHandler import PageHandler

class HistoryHandler(PageHandler):

    def __init__(self):
        super(HistoryHandler, self).__init__('history')

    def getHTML(self, controller, parameter):
        return super(HistoryHandler, self).getHTML(controller, parameter)