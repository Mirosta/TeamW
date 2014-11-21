import jinja2
import os
import logging
from exceptions import NoTemplateError

# Class for representing URL parameters for pages
class Parameter(object):
    
    class Type(object):
        Int = object()
        String = object()
        NoParameter = object()

    Invalid = object()
    NoneGiven = object()

    def __init__(self, paramType = Type.NoParameter, isRequired = False, canBeInvalid = False):
        self.paramType = paramType
        self.required = isRequired
        self.beInvalid = canBeInvalid
        
    def getType(self):
        return self.paramType
        
    def isRequired(self):
        return self.required
        
    def canBeInvalid(self):
        return self.beInvalid

# Class for handling content - be it pages or verbs
class ContentHandler(object):
    
    TEMPLATE_EXTENSION = '.jinja'
    TEMPLATE_FOLDER = '../view/'
    JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), TEMPLATE_FOLDER)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=False
    )
    
    def __init__(self, templateFile):
        self.templateFile = templateFile
    
    def getHTML(self, controller, parameter):
        return self.renderTemplate(self.templateFile)

    def renderTemplate(self, templateFile):
        # Get the template and render it
        if templateFile == None: raise NoTemplateError()
        template = ContentHandler.JINJA_ENVIRONMENT.get_template(templateFile + ContentHandler.TEMPLATE_EXTENSION)
        return template.render({'page': self})
        
    def postHTML(self, controller, parameter):
        # Need to error out here
        pass
    
    def getAPI(self, controller, parameter):
        # Need to error out here
        pass
        
    def postAPI(self, controller, parameter):
        # Need to error out here
        pass

# Class for handling pages
class PageHandler(ContentHandler):
    
    def __init__(self, templateFile = None, parameter = Parameter(), verbs = {}):
        super(PageHandler, self).__init__(templateFile)
        self.parameter = parameter
        self.verbs = verbs
    
    def hasVerb(self, verb):
        return self.verbs.has_key(verb)
        
    def getVerb(self, verb):
        return self.verbs.get(verb)
    
    def getParameter(self):
        return self.parameter
        
    def validateParameter(self, parameter):
        if self.getParameter().getType() == Parameter.Type.NoParameter:
            return parameter == Parameter.NoneGiven
        
        if self.getParameter().getType() == Parameter.Type.Int:
            try:
                val = int(parameter)
                return True
            except ValueError:
                return False
        
        return True
        
# class for handling verbs
class VerbHandler(ContentHandler):

    def __init__(self, templateFile):
        super(VerbHandler, self).__init__(templateFile)
    
# Test page with a test template
class TestPageHandler(PageHandler):

    def __init__(self):
        super(TestPageHandler, self).__init__('test')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)
