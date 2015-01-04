from payme.controller.globals import Global
import sys, traceback

# Super class for all application exceptions
class PaymeError(Exception):
    codes = {
        404: 'Page not found',
        403: 'Permission denied',
        500: 'Internal server error',
        400: 'Bad request',
    }

    def __init__(self, errorCode):
        self.errorCode = errorCode
        
    def __init__(self, errorType):
        self.errorType = errorType
        
    def getErrorCode(self):
        return self.errorCode
        
    def getErrorMessage(self):
        if Global.debug:
            return traceback.format_exc()
        else:
            return codes[self.getErrorCode()]

# Page not found - 404
class NotFoundError(PaymeError):
    def __init__(self):
        super(NotFoundError, self).__init__(404)

# Permission denied - 403
class PermissionDeniedError(PaymeError):
    def __init__(self):
        super(PermissionDeniedError, self).__init__(403)

# Internal error - 500
class InternalError(PaymeError):
    def __init__(self):
        super(InternalError, self).__init__(500)
        
# Bad request - 400
class BadRequestError(PaymeError):
    def __init__(self):
        super(BadRequestError, self).__init__(400)

class InvalidParameterError(BadRequestError):
    pass

class PageNotFoundError(NotFoundError):
    pass

class MissingFieldError(PaymeError):
    def __init__(self):
        super(OwnerInGroupError, self).__init__(PaymeError.Types.SERVER_ERROR)

class AttributeNotFound(PaymeError):
    def __init__(self):
        super(AttributeNotFound, self).__init__(PaymeError.Types.SERVER_ERROR)

class UpdateNotAllowed(PaymeError):
    def __init__(self):
        super(UpdateNotAllowed, self).__init__(PaymeError.Types.SERVER_ERROR)class NoTemplateError(InternalError):
    pass

class SecurityError(PermissionDeniedError):
    pass

class OAuthCodeError(InternalError):
    pass

class OwnerInGroupError(InternalError):
    pass

class MissingFieldError(InternalError):
    pass
        
class UnsupportedMethod(InternalError):
    pass
