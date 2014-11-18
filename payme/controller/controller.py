import webapp2
import logging
from contentHandler import ContentHandler, ParameterType
# /api/<page>(/<verb:w+>)? -> apiController
# /<page>(/<verb:w+>)? -> htmlController

# /<page>/* -> controller->handleHTML
# controller->handlePage(api, page)
#/foo/1
#/groups/edit/
#/groups/edit/1
# controller

# apiController
    #get super.get(true, page, verb, param)
    #post super.post(true, params)
# htmlController
    #get super.get(api=false, params)
    #post - error
from exceptions import PageNotFound

class HTTPVerb:
    GET = object()
    POST = object()

class Controller (webapp2.RequestHandler):

    pages = {'home': ContentHandler()}
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

        if verbName not in page.getVerbs():
            contentHandler = page
            parameter = verbName
            if parameter == "" and page.isParameterRequired(): raise PageNotFound('404 Page not found')
            if parameter != "" and not self.validateParameter(page, verbName):
                if not page.allowInvalidParameter(): raise PageNotFound('404 Page not found')
                else: parameter = None
        elif verbName in page.getVerbs():
            contentHandler = page.getVerbs()[verbName]
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
        if page.getParameterType() == ParameterType.NoParameter: return False
        if page.getParameterType() == ParameterType.Int:
            try:
                val = int(parameter)
                return True
            except ValueError:
                return False
        return True

class HTMLController(Controller):
    def __init__(self, request = None, response = None):
        super(HTMLController, self).__init__(False)
        super(Controller, self).__init__(request, response)

class APIController(Controller):
    def __init__(self, request = None, response = None):
        super(HTMLController, self).__init__(True)
        super(Controller, self).__init__(request, response)

logging.getLogger().setLevel(logging.DEBUG)
logging.debug('Loaded controller')
routes = webapp2.WSGIApplication(
    [
        #webapp2.Route(r'/api/<pageName:\w+>/(?:/<verbName:\w+>)?/?', APIController, 'api'),
        webapp2.SimpleRoute(r'^/(\w+)(?:/(\w+))?/?', HTMLController, 'html'),
        #webapp2.Route(r'/', webapp2.RedirectHandler, defaults={'_uri': '/' + Controller.homePage})
    ], debug=True)
