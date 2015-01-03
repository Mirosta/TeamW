import logging
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.controller.exceptions import OAuthCodeError


class Scope:

    Email = 'email'
    OpenID = 'openid'

class OAuthHandler(PageHandler):

    def __init__(self):
        super(OAuthHandler, self).__init__(None, Parameter(), {'login': OAuthLoginHandler(), 'callback': OAuthCallbackHandler()})

class OAuthLoginHandler(VerbHandler):
    REDIRECT_URI = 'http://localhost:8080/oauth/callback'
    CLIENT_ID = '399506081912-4dg74rjo7k6huk0f5bsid5tst65qd7c2.apps.googleusercontent.com'
    CLIENT_SECRET = 'Ih38GJ4bMO9TTDuhPpYKv9rS'
    oAuthFlow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, str.join(' ',[Scope.OpenID, Scope.Email]), redirect_uri=REDIRECT_URI)

    def __init__(self):
        super(OAuthLoginHandler, self).__init__(None)

    def getHTML(self, controller, parameter):
        self.authorise(controller)

    def authorise(self, controller, scopes = [Scope.OpenID, Scope.Email]):
        OAuthLoginHandler.oAuthFlow.scope = str.join(' ', scopes)
        logging.info('Redirecting')
        redirectTo = OAuthLoginHandler.oAuthFlow.step1_get_authorize_url()
        controller.redirect(redirectTo)

class OAuthCallbackHandler(VerbHandler):

    def __init__(self):
        super(OAuthCallbackHandler, self).__init__(None)
        self.errorMessage = ''
        self.credentials = None

    def getHTML(self, controller, parameter):
        try:
            self.credentials = self.handleCode(controller, parameter)
            controller.onLogin(self.credentials)

            return self.renderTemplate('oAuthSuccess')
        except (OAuthCodeError, FlowExchangeError) as ex:
            self.errorMessage = ex.message
            return self.renderTemplate('oAuthCodeError')

    def handleCode(self, controller, parameter):
        if controller.request.GET.has_key('error'):
            raise OAuthCodeError() #controller.request.GET['error']
        if not controller.request.GET.has_key('code'):
            raise OAuthCodeError() #'No code given'
        return OAuthLoginHandler.oAuthFlow.step2_exchange(controller.request.GET['code'])