# Super class for all application exceptions
class PaymeError(Exception):
    class Types:
        NOT_FOUND = 404
        PERMISSION_DENIED = 403
        SERVER_ERROR = 500
        
    def __init__(self, errorType):
        self.errorType = errorType
        
    def getErrorCode():
        return self.errorType

class PageNotFoundError(PaymeError):
    def __init__(self):
        super(PageNotFoundError, self).__init__(PaymeError.Types.NOT_FOUND)

class NoTemplateError(PaymeError):
    def __init__(self):
        super(PageNotFoundError, self).__init__(PaymeError.Types.SERVER_ERROR)

