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
    TEMPLATE_FOLDER = '/../view/'
    JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + TEMPLATE_FOLDER),
        extensions=['jinja2.ext.autoescape'],
        autoescape=False)
    
    def __init__(self, templateFile):
        self.templateFile = templateFile
    
    def getHTML(self, parameter):
        logging.info('Loading template from ' + __file__)
        # Get the template and render it
        if self.templateFile == None: raise NoTemplateError("No template set on content handler")
        template = ContentHandler.JINJA_ENVIRONMENT.get_template(self.templateFile + ContentHandler.TEMPLATE_EXTENSION)
        return template.render({'page': self})
        
    def postHTML(self, parameter):
        # Need to error out here
        pass
    
    def getAPI(self, parameter):
        # Need to error out here
        pass
        
    def postAPI(self, parameter):
        # Need to error out here
        pass

# Class for handling pages
class PageHandler(ContentHandler):
    
    def __init__(self, templateFile = None, parameter = Parameter(), verbs = {}):
        super(PageHandler, self).__init__(templateFile)
        self.parameter = parameter
        self.verbs = verbs
    
    def getVerb(self, verb):
        return self.verbs.has_key(verb)
        
    def hasVerb(self, verb):
        return self.verbs.get(verb)
    
    def getParameter(self):
        return self.parameter
        
# class for handling verbs
class VerbHandler(ContentHandler):

    def __init__(self, templateFile):
        super(VerbHandler, self).__init__(templateFile)
    

# Test page with a test template
class TestPageHandler(PageHandler):

    def __init__(self):
        super(TestPageHandler, self).__init__('test')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)
