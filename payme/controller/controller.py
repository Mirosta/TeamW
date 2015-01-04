import logging
from google.appengine.ext.ndb.key import Key

import webapp2
import httplib2

from webapp2_extras import sessions
from webapp2_extras.appengine.sessions_memcache import MemcacheSessionFactory

from contentHandler import Parameter
from payme.controller.pages.homepageHandler import HomepageHandler
from payme.controller.pages.helpHandler import HelpHandler
from payme.controller.pages.historyHandler import HistoryHandler
from dbTesting import TestPage
from exceptions import PageNotFoundError, InvalidParameterError
from payme.controller.pages.friendHandler import FriendHandler
from payme.controller.pages.groupHandler import GroupHandler
from payme.controller.pages.oAuthLogin import OAuthLoginHandler, OAuthHandler
from payme.model.user import User
from apiclient.discovery import build

from payme.controller.builddb import BuildDB

# Supported HTTP verbs
from payme.controller.pages.userHandler import UserHandler
from payme.controller.pages.debtHandler import DebtHandler
from payme.controller.pages.paymentsHandler import PaymentsHandler
from payme.controller.pages.notificationHandler import NotificationHandler

from payme.controller.globals import Global

class HTTPVerb:
    GET = object()
    POST = object()

apiKeys = {'oAuth2': None}
serviceHttp = httplib2.Http()
userInfoService = build('oauth2', 'v2', http=serviceHttp)
# Main controller. Handles the map of pages and what not.
class Controller (webapp2.RequestHandler):

    pages = {
        'home': HomepageHandler(),
        'oauth': OAuthHandler(),
        'test': TestPage(),
        'friends': FriendHandler(),
        'groups': GroupHandler(),
        'user': UserHandler(),
        'debt': DebtHandler(),
        'payments': PaymentsHandler(),
        'help': HelpHandler(),
        'history': HistoryHandler(),
        'notifications': NotificationHandler(),
        'builddb': BuildDB()
    }

    homePage = 'home'
    loginPage = '/user/login'

    def __init__(self, isAPI):
        self.isAPI = isAPI
        self.currentUser = None

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
        return self.session_store.get_session(backend='memcache')

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
            if contentHandler.accessLevel > self.getAccessLevel(): #Redirect to login if necessary
                if httpVerb == HTTPVerb.GET:
                    self.session['redirectTo'] = '/' + pageName + '/' + verbName
                self.redirect(self.loginPage)
                return
        # Otherwise check if pages accepts parameters
        else:
            contentHandler = page
            parameter = verbName

            if contentHandler.accessLevel > self.getAccessLevel(): #Redirect to login if necessary
                if httpVerb == HTTPVerb.GET:
                    self.session['redirectTo'] = '/' + pageName + '/' + verbName
                self.redirect(self.loginPage)
                return

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
            elif httpVerb == HTTPVerb.POST: return contentHandler.postAPI(self, parameter, self.request.body)
        else:
            if httpVerb == HTTPVerb.GET: return contentHandler.getHTML(self, parameter)
            elif httpVerb == HTTPVerb.POST: return contentHandler.postHTML(self, parameter, self.request.POST)

    #We have credentials, now do something with them
    def onLogin(self, credentials):
        credentials.authorize(serviceHttp)
        userDetails = userInfoService.userinfo().get().execute()
        existingUser = User.query(User.googleID == userDetails['id']).fetch()
        if existingUser.__len__() < 1: #No users found
            self.onNewUserLogin(userDetails, credentials)
        else:
            self.onExistingUserLogin(existingUser[0], userDetails, credentials)

    def onNewUserLogin(self, userDetails, credentials):
        newUser = User(googleID = userDetails['id'], email = userDetails['email'], name = userDetails['given_name'], familyName = userDetails['family_name'], profilePicture = userDetails['picture'], credentials = credentials)
        newUser.put()
        self.session['user'] = newUser.key.urlsafe()

    def onExistingUserLogin(self, existingUser, userDetails, credentials):
        existingUser.credentials = credentials
        existingUser.put()
        self.session['user'] = existingUser.key.urlsafe()

    def getCurrentUser(self):
        if self.currentUser == None:
            if not 'user' in self.session:
                return None
            else:
                matchingUsers = User.query(User.key == Key(urlsafe=self.session['user'])).fetch()
                if matchingUsers.__len__() < 1:
                    return None
                else:
                    self.currentUser = matchingUsers[0]
        return self.currentUser

    def getAccessLevel(self):
        user = self.getCurrentUser()
        if user == None:
            return 0
        else:
            return 1

# Controller for handling HTML requests
class HTMLController(Controller):
    def __init__(self, request = None, response = None):
        super(HTMLController, self).__init__(False)
        super(Controller, self).__init__(request, response)
        Global.htmlController = self

# Controller for handling API requests
class APIController(Controller):
    def __init__(self, request = None, response = None):
        super(APIController, self).__init__(True)
        super(Controller, self).__init__(request, response)
        Global.apiController = self

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'a different random key',
     'backends': {'datastore': 'webapp2_extras.appengine.sessions_ndb.DatastoreSessionFactory',
                 'memcache': 'webapp2_extras.appengine.sessions_memcache.MemcacheSessionFactory',
                 'securecookie': 'webapp2_extras.sessions.SecureCookieSessionFactory'
                 }
}
#TODO: Maybe something a little more secure

logging.debug('Loaded controller')

# Define the routes.
routes = webapp2.WSGIApplication([
    webapp2.SimpleRoute(r'^/api/(\w+)(?:/(\w+))?/?', APIController, 'api'),
    webapp2.SimpleRoute(r'^/(\w+)(?:/(\w+))?/?', HTMLController, 'html'),
    webapp2.Route(r'/', webapp2.RedirectHandler, defaults={'_uri': '/' + Controller.homePage}),
], debug=True, config=config)

