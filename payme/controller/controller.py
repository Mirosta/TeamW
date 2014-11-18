import webapp2
import logging
from contentHandler import TestPageHandler, Parameter
from exceptions import PageNotFound

# Supported HTTP verbs
class HTTPVerb:
    GET = object()
    POST = object()

# Main controller. Handles the map of pages and what not.
class Controller (webapp2.RequestHandler):

    pages = {'home': TestPageHandler()}
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
            raise PageNotFound('404 Page not found')
        page = Controller.pages[pageName]

        contentHandler = None
        parameter = None

        if not page.hasVerb(verbName):
            contentHandler = page
            parameter = verbName
            if parameter == "" and page.getParameter().isRequired(): raise PageNotFound('404 Page not found')
            if parameter != "" and not self.validateParameter(page, verbName):
                if not page.getParameter().canBeInvalid(): raise PageNotFound('404 Page not found')
                else: parameter = None
        elif page.hasVerb(verbName):
            contentHandler = page.getVerb(verbName)
        else:
            raise PageNotFound('404 Page not found')

        response = self.sendToContentHandler(contentHandler, parameter, httpVerb)
        self.response.write(response)

    def sendToContentHandler(self, contentHandler, parameter, httpVerb):
        if self.isAPI:
            if httpVerb == HTTPVerb.GET: return contentHandler.getAPI(parameter)
            elif httpVerb == HTTPVerb.POST: return contentHandler.postAPI(parameter)
        else:
            if httpVerb == HTTPVerb.GET: return contentHandler.getHTML(parameter)
            elif httpVerb == HTTPVerb.POST: return contentHandler.postHTML(parameter)

    def validateParameter(self, page, parameter):
        #Do validation
        if page.getParameter.getType() == Parameter.Type.NoParameter: return False
        if page.getParameter.getType() == Parameter.Type.Int:
            try:
                val = int(parameter)
                return True
            except ValueError:
                return False
        return True

# Controller for handling HTML requests
class HTMLController(Controller):
    def __init__(self, request = None, response = None):
        super(HTMLController, self).__init__(False)
        super(Controller, self).__init__(request, response)

# Controller for handling API requests
class APIController(Controller):
    def __init__(self, request = None, response = None):
        super(HTMLController, self).__init__(True)
        super(Controller, self).__init__(request, response)

# Set debu logging
logging.getLogger().setLevel(logging.DEBUG)
logging.debug('Loaded controller')

# Define the routes.
routes = webapp2.WSGIApplication([
    webapp2.Route(r'^/api/(\w+)(?:/(\w+))?/?', APIController, 'api'),
    webapp2.SimpleRoute(r'^/(\w+)(?:/(\w+))?/?', HTMLController, 'html'),
    webapp2.Route(r'/', webapp2.RedirectHandler, defaults={'_uri': '/' + Controller.homePage})
], debug=True)
