#/api/groups -> json
#/groups -> html
#ContentHandler
    #Type of argument
    #Required
#PageHandler /groups page
#   Map<String, VerbHandler> verbHandlers add
#VerbHandler /groups/add
#   getApi
#   getHtml
#   postApi
#   postHtml
class ParameterType:
    Int = object()
    String = object()
    NoParameter = object()

class ContentHandler:

    #TODO: Remove dummy code Start
    def getHTML(self, parameter):
        if parameter == None: body = '<div style="color: red;">Invalid Parameter</div>'
        elif parameter == "": body = 'Lol no parameter'
        else: body = "Hello world number " + parameter

        return "<html><body>" + body + "</body></html>"

    def getAPI(self, parameter):
        return "{message: 'Hello World'}"

    def getVerbs(self):
        return {}

    def getParameterType(self):
        return ParameterType.Int

    def isParameterRequired(self):
        return False

    def allowInvalidParameter(self):
        return True
    #TODO: End

class PageHandler(ContentHandler):

    def __init__(self, verbs = {}):
        self.verbs = verbs

    def getVerbs(self):
        return self.verbs

class MyPage(PageHandler):

    verbs = {}

    def __init__(self):
        super(MyPage, self).__init__(self.verbs)