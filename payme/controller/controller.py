import webapp2
import logging
from webapp2 import Route
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

    pages = {}

    def __init(self):
        self.isAPI = False
        pass

    def get(self, pageName, verbName):
        logging.debug('GET Request with route %s', self.request.route.name)
        self.handleRequest(HTTPVerb.GET, pageName, verbName)

    def post(self, pageName, verbName):
        self.handleRequest(HTTPVerb.POST, pageName, verbName)

    def handleRequest(self, httpVerb, pageName = None, verbName = None):
        if pageName not in Controller.pages:
            raise PageNotFound('404 Page not found')
        page = Controller.pages[pageName]

        contentHandler = None
        parameter = None

        if verbName not in page.getVerbs() and self.validateParameter(page, verbName):
            contentHandler = page
            parameter = verbName
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

        return True

logging.getLogger().setLevel(logging.DEBUG)
routes = webapp2.WSGIApplication([Route('/api/<pageName:w+>/<verbName:w+>', handler = 'Controller', name='apiPath'), Route('/<pageName:w+>/<verbName:w+>', handler = 'Controller', name = 'htmlPath')], debug=True)
