from payme.controller.contentHandler import PageHandler, Parameter
from payme.controller.exceptions import PaymeError

# Page for handling errors.
class ErrorHandler(PageHandler):
    
    def __init__(self):
        super(ErrorHandler, self).__init__('error')
        
        # Optional parameter
        self.parameter = Parameter(Parameter.Type.Int, False, False)
        
    def getHTML(self, controller, parameter):
        self.isInternal = False
        return super(ErrorHandler, self).getHTML(controller, parameter)
        
    def handleError(self, controller, exception):
        self.isInternal = True
        self.exception = exception
        return self.renderTemplate(controller, self.templateFile)
    
    # Get the error code of the page
    def getErrorCode(self):
        if self.isInternal:
            return self.exception.getErrorCode()
        else:
            return self.getParameter()
        
    # Get the error message of the page
    def getErrorMessage(self):
        if self.isInternal:
            return self.exception.getErrorMessage()
        else:
            return PaymeError.codes[self.getErrorCode()]

