import jinja2
import os
import logging
from exceptions import NoTemplateError

import json
from datetime import date, datetime

from google.appengine.ext import ndb
from payme.model.user import User

FOOTER = "footer"
HEADER = "header"

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
    
    def __init__(self, templateFile, accessLevel = 1):
        self.templateFile = templateFile
        self.accessLevel = accessLevel
        self.lastController = None
    
    def getHTML(self, controller, parameter):
        self.lastController = controller
        return self.renderTemplate(controller, self.templateFile)

    def renderTemplate(self, controller, templateFile):
        # Get the template and render it
        self.lastController = controller
        if templateFile == None: raise NoTemplateError()
        template = ContentHandler.JINJA_ENVIRONMENT.get_template(templateFile + ContentHandler.TEMPLATE_EXTENSION)
        return template.render({'page': self, 'controller': controller})
        
    def postHTML(self, controller, parameter):
        self.lastController = controller
        # Need to error out here
        pass
    
    def getAPI(self, controller, parameter):
        self.lastController = controller
        # Need to error out here
        pass
        
    def postAPI(self, controller, parameter):
        self.lastController = controller
        # Need to error out here
        pass

    def header(self):
        logging.info(self.lastController)
        return self.renderTemplate(self.lastController, HEADER)

    def footer(self):
        return self.renderTemplate(self.lastController, FOOTER)

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

    # This encoder ensures that complex data type are converted
    # for JSON serialisation
    class JSonAPIEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, date) or isinstance(obj, datetime):
                return obj.strftime('%Y/%m/%d %H:%M:%S')
            elif isinstance(obj, ndb.Key):
                return obj.urlsafe()
            elif isinstance(obj, ndb.Model):
                return obj.to_dict()
            else:
                return json.JSONEncoder.default(self, obj)

    # Helper function to ease serialisation
    def serialize(self, object_to_serialize):
        return json.dumps(object_to_serialize, cls=self.JSonAPIEncoder)

    # Helper function to query user and handles user not found
    def queryUser(self, key):
        user = User.query(User.key == key).fetch(10)

        # If database returns nothing
        if user.__len__() != 0:
            return user[0]
        else:
            return '{error: "User not found"}'
        
# class for handling verbs
class VerbHandler(ContentHandler):

    def __init__(self, templateFile):
        super(VerbHandler, self).__init__(templateFile)
    
# Test page with a test template
class TestPageHandler(PageHandler):

    def __init__(self):
        super(TestPageHandler, self).__init__('test')
        self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    def getHTML(self, controller, parameter):
        return super(TestPageHandler, self).getHTML(controller, parameter)

