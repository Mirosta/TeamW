import json
import logging

import webapp2
import httplib2

from webapp2_extras import sessions

from contentHandler import TestPageHandler, Parameter
from dbTesting import TestPage
from exceptions import PageNotFoundError, InvalidParameterError
from payme.controller.pages.friendHandler import FriendHandler
from payme.controller.pages.groupHandler import GroupHandler
from payme.controller.pages.oAuthLogin import OAuthLoginHandler, OAuthHandler
from payme.model.user import User
from apiclient.discovery import build

# Supported HTTP verbs
from payme.controller.pages.userHandler import UserHandler
from payme.controller.pages.debtHandler import DebtHandler
from payme.controller.pages.transactionsHandler import TransactionsHandler


class HTTPVerb:
    GET = object()
    POST = object()

apiKeys = {'oAuth2': None}
htmlController = None
apiController = None
serviceHttp = httplib2.Http()
userInfoService = build('oauth2', 'v2', http=serviceHttp)
# Main controller. Handles the map of pages and what not.
class Controller (webapp2.RequestHandler):

    pages = {
        'home': TestPageHandler(),
        'oauth': OAuthHandler(),
        'test': TestPage(),
        'friends': FriendHandler(),
        'groups': GroupHandler(),
        'user': UserHandler(),
        'debt': DebtHandler(),
        'transactions': TransactionsHandler(),
    }

    homePage = 'home'

    def __init__(self, isAPI):
        self.isAPI = isAPI

    #Session Stuff
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def get(self, pageName, verbName):
        self.handleRequest(HTTPVerb.GET, pageName, verbName)

    def post(self, pageName, verbName):
        self.handleRequest(HTTPVerb.POST, pageName, verbName)

    def handleRequest(self, httpVerb, pageName, verbName):
        if verbName == None: verbName = ''

        if pageName not in Controller.pages:
            raise PageNotFoundError()
            
        page = Controller.pages[pageName]

        contentHandler = None
        parameter = None

        # If the page has a verb with that name, use that
        if page.hasVerb(verbName):
            contentHandler = page.getVerb(verbName)
            
        # Otherwise check if pages accepts parameters
        else:
            contentHandler = page
            parameter = verbName
            
            if parameter == "":
                if page.getParameter().isRequired():
                    raise InvalidParameterError()
                else:
                    parameter = Parameter.NoneGiven
            else:
                # If the parameter is invalid, and this isn't allowed, throw an error. Otherwise mark the param as invalid.
                if not page.validateParameter(parameter):
                    if page.getParameter().canBeInvalid():
                        parameter = Parameter.Invalid
                    else:
                        raise InvalidParameterError()

        response = self.sendToContentHandler(contentHandler, parameter, httpVerb)

        if response != None:
            self.response.write(response)

    def sendToContentHandler(self, contentHandler, parameter, httpVerb):
        logging.info('Content Handler: ' + contentHandler.__str__())
        if self.isAPI:
            if httpVerb == HTTPVerb.GET: return contentHandler.getAPI(self, parameter)
            elif httpVerb == HTTPVerb.POST: return contentHandler.postAPI(self, parameter)
        else:
            if httpVerb == HTTPVerb.GET: return contentHandler.getHTML(self, parameter)
            elif httpVerb == HTTPVerb.POST: return contentHandler.postHTML(self, parameter)

    #We have credentials, now do something with them
    def onLogin(self, credentials):
        credentials.authorize(serviceHttp)
        userDetails = userInfoService.userinfo().get().execute()
        logging.log(logging.INFO, json.dumps(userDetails))

    def getCurrentUser(self):
        if not 'user' in self.session:
            return None
        else:
            matchingUsers = User.query(User.key == self.session['currentUser']).fetch()
            if matchingUsers.__len__() < 1:
                return None
            else:
                return matchingUsers[0]

# Controller for handling HTML requests
class HTMLController(Controller):
    def __init__(self, request = None, response = None):
        super(HTMLController, self).__init__(False)
        super(Controller, self).__init__(request, response)
        htmlController = self

# Controller for handling API requests
class APIController(Controller):
    def __init__(self, request = None, response = None):
        super(APIController, self).__init__(True)
        super(Controller, self).__init__(request, response)
        apiController = self

sessions.default_config['secret_key'] = 'a random key to use for generating cookies' #TODO: Maybe something a little more secure
logging.debug('Loaded controller')

# Define the routes.
routes = webapp2.WSGIApplication([
    webapp2.SimpleRoute(r'^/api/(\w+)(?:/(\w+))?/?', APIController, 'api'),
    webapp2.SimpleRoute(r'^/(\w+)(?:/(\w+))?/?', HTMLController, 'html'),
    webapp2.Route(r'/', webapp2.RedirectHandler, defaults={'_uri': '/' + Controller.homePage}),
], debug=True)

