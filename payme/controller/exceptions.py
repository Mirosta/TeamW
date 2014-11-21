# Super class for all application exceptions
class PaymeError(Exception):
    class Types:
        NOT_FOUND = 404
        PERMISSION_DENIED = 403
        SERVER_ERROR = 500
        BAD_REQUEST = 400
        
    def __init__(self, errorType):
        self.errorType = errorType
        
    def getErrorCode():
        return self.errorType

class InvalidParameterError(PaymeError):
    def __init__(self):
        super(InvalidParameterError, self).__init__(PaymeError.Types.BAD_REQUEST)

class PageNotFoundError(PaymeError):
    def __init__(self):
        super(PageNotFoundError, self).__init__(PaymeError.Types.NOT_FOUND)

class NoTemplateError(PaymeError):
    def __init__(self):
        super(NoTemplateError, self).__init__(PaymeError.Types.SERVER_ERROR)

class OAuthCodeError(PaymeError):
    def __init__(self):
        super(OAuthCodeError, self).__init__(PaymeError.Types.SERVER_ERROR)
