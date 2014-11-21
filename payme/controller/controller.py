import webapp2
import logging
from contentHandler import TestPageHandler, Parameter
from dbTesting import TestPage
from exceptions import PageNotFoundError, InvalidParameterError
from oAuthLogin import OAuthLoginHandler
from pages import *

# Supported HTTP verbs
class HTTPVerb:
    GET = object()
    POST = object()

# Main controller. Handles the map of pages and what not.
class Controller (webapp2.RequestHandler):

    pages = {
        'home': TestPageHandler(),
        'login': OAuthLoginHandler(),
        'test': TestPage()
    }
    
    homePage = 'home'

    def __init__(self, isAPI):
        self.isAPI = isAPI

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
                parameter = Parameter.NoneGiven
            
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

# Controller for handling HTML requests
class HTMLController(Controller):
    def __init__(self, request = None, response = None):
        super(HTMLController, self).__init__(False)
        super(Controller, self).__init__(request, response)

# Controller for handling API requests
class APIController(Controller):
    def __init__(self, request = None, response = None):
        super(APIController, self).__init__(True)
        super(Controller, self).__init__(request, response)

logging.debug('Loaded controller')

# Define the routes.
routes = webapp2.WSGIApplication([
    webapp2.SimpleRoute(r'^/api/(\w+)(?:/(\w+))?/?', APIController, 'api'),
    webapp2.SimpleRoute(r'^/(\w+)(?:/(\w+))?/?', HTMLController, 'html'),
    webapp2.Route(r'/', webapp2.RedirectHandler, defaults={'_uri': '/' + Controller.homePage}),
], debug=True)

