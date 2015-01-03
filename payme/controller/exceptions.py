# Super class for all application exceptions
class PaymeError(Exception):
    class Types:
        NOT_FOUND = 404
        PERMISSION_DENIED = 403
        SERVER_ERROR = 500
        BAD_REQUEST = 400
        
    def __init__(self, errorType):
        self.errorType = errorType
        
    def getErrorCode(self):
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

class SecurityError(PaymeError):
    def __init__(self):
        super(SecurityError, self).__init__(PaymeError.Types.PERMISSION_DENIED)

class OAuthCodeError(PaymeError):
    def __init__(self):
        super(OAuthCodeError, self).__init__(PaymeError.Types.SERVER_ERROR)

class OwnerInGroupError(PaymeError):
    def __init__(self):
        super(OwnerInGroupError, self).__init__(PaymeError.Types.SERVER_ERROR)
