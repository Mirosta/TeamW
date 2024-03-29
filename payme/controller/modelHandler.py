import json
import logging
from jinja2 import utils
from operator import itemgetter
from google.appengine.ext import ndb
from google.appengine.ext.ndb import Key
from payme.controller import validator
from payme.controller.contentHandler import PageHandler, Parameter, VerbHandler
from datetime import date, datetime

from payme.controller.exceptions import InvalidVerbType, AddNotAllowed
from payme.controller.globals import Global


class RelatedModel:

    def __init__(self, modelClass, referencingModelField, jsonFieldName):
        self.modelClass = modelClass
        self.referencingModelField = referencingModelField
        self.jsonFieldName = jsonFieldName
        self.resolvedClass = None

    def getModelField(self):
        return getattr(self.modelClass, self.referencingModelField)

class ReadOnlyFunction:

    def __init__(self, functionName, jsonFieldName):
        self.functionName = functionName
        self.jsonFieldName = jsonFieldName

class ModelHandler(PageHandler):

    def __init__(self, view, verbs, getAllFunction, modelClass, relatedModels = [], readOnlyFunctions = [], hiddenFields = []):
        #logging.info("Setting template file " + view.__str__())
        super(ModelHandler, self).__init__(view, Parameter(Parameter.Type.String), verbs)

        requiredVerbs = [('add', ModelAddHandler, [modelClass]), ('remove', ModelRemoveHandler, [modelClass]),
                         ('update', ModelUpdateHandler, [modelClass])]

        for requiredVerb in requiredVerbs:
            if verbs.has_key(requiredVerb[0]):
                if not isinstance(verbs[requiredVerb[0]], requiredVerb[1]):
                    raise InvalidVerbType
            else:
                verbs[requiredVerb[0]] = requiredVerb[1](None)
            verbs[requiredVerb[0]].setup(*requiredVerb[2])

        self.getAllFunction = getAllFunction
        self.modelClass = modelClass
        self.relatedModels = relatedModels#[RelatedModel(Payment, 'debt', 'payments')]
        self.readOnlyFunctions = readOnlyFunctions #example: [ReadOnlyFunction('getOE','netAmount'), ReadOnlyFunction('getCR','Owe'), ReadOnlyFunction('getDR', 'Own')]
        self.hiddenFields = hiddenFields

    def getRequestParameter(self, controller, parameterName, default, paramType):
        if controller.request.get(parameterName) != "":
                validationParameter = Parameter(paramType, False, True)
                if validationParameter.validate(controller.request.get(parameterName)):
                    return validationParameter.cast(controller.request.get(parameterName))

        return default

    #Called by the controller when someone visits a /api/ link
    def getAPI(self, controller, parameter):
        if parameter == Parameter.NoneGiven: #If no parameter is given, assume they want all
            count = self.getRequestParameter(controller, "count", None, Parameter.Type.Int)
            offset = self.getRequestParameter(controller, "offset", 0, Parameter.Type.Int)
            sortBy = self.getRequestParameter(controller, "sortBy", None, Parameter.Type.String)
            return self.getAll(controller, count, offset, sortBy)
        if parameter == Parameter.Invalid:
            return self.onInvalidParameter() # change
        # if int(parameter) != 1:
        #     return self.onUnknownFriend() # change
        logging.info("Parameter: " + str(parameter))
        return self.getOne(controller, parameter) #If a parameter is given and is valid, lookup by the key given

    #Gets all model instances
    def getAll(self, controller, count = None, offset = 0, sortBy = None):
        currentUser = controller.getCurrentUser()
        function = getattr(currentUser, self.getAllFunction)
        models = function()
        modelsOutput = []

        for model in models:
            data = self.getOneInner(controller, model)

            modelsOutput.append(data)
        logging.info('From: ' + str(offset) + " to: " + str(count))
        end = None
        if not count is None:
            end = offset + count
        modelsOutput = modelsOutput[offset:end]
        if not sortBy is None:
            reversed = sortBy[0] == '-'
            logging.info("Reversed? " + str(reversed))
            if reversed:
                sortBy = sortBy[1:]
            modelsOutput = sorted(modelsOutput, key=itemgetter(sortBy))
            if reversed:
                modelsOutput.reverse()
        return self.serialize({'results': modelsOutput})

    #Get one model instance by ID
    def getOne(self, controller, parameter):
        models = self.modelClass.query(self.modelClass.key == Key(urlsafe=parameter)).fetch()
        if models.__len__() < 1:
            return self.onModelNotFound()
        data = self.getOneInner(controller, models[0])
        return self.serialize(data)

    def getOneInner(self, controller, model):
        data = model.to_dict()
        data['key'] = model.key

        for hiddenField in self.hiddenFields:
            if data.has_key(hiddenField):
                data.pop(hiddenField)

        data['readOnly'] = {}

        for relatedModel in self.relatedModels:
            relatedValues = relatedModel.modelClass.query(relatedModel.getModelField() == model.key)
            jsonOutput = []

            for relatedValue in relatedValues:
                jsonOutput.append(relatedValue.key)
            data['readOnly'][relatedModel.jsonFieldName] = jsonOutput

        for readOnlyFunction in self.readOnlyFunctions:
            function = getattr(model, readOnlyFunction.functionName)
            value = function()
            data['readOnly'][readOnlyFunction.jsonFieldName] = value

        return data

    def onInvalidParameter(self):
        return '{error: "Invalid key"}'

    def onModelNotFound(self):
        return '{error: "Key not found"}'

    # Helper function to ease serialisation
    def serialize(self, object_to_serialize):
        return json.dumps(object_to_serialize, cls=ModelHandler.JSonAPIEncoder)

    # This encoder ensures that complex data type are converted
    # for JSON serialisation
    class JSonAPIEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, date) or isinstance(obj, datetime):
                return obj.strftime(Global.JSONDateTime)
            elif isinstance(obj, ndb.Key):
                return obj.urlsafe()
            elif isinstance(obj, ndb.Model):
                return obj.to_dict()
            elif isinstance(obj, str):
                return json.JSONEncoder.default(self, str(utils.escape(obj)))
            else:
                return json.JSONEncoder.default(self, obj)

            
class ModelAddHandler(VerbHandler):

    def __init__(self, view = None):
        super(ModelAddHandler, self).__init__(view)

    def setup(self, type):
        self.type = type

    def postAPI(self, controller, parameter, postData):
        try:
            entity = validator.create(postData, self.type)
            # add new entity to database
            entity.put()
            return '{"success": 1}'
        except Exception as e:
            raise e

class ModelRemoveHandler(VerbHandler):

    def __init__(self, view = None):
        super(ModelRemoveHandler, self).__init__(view)

    def setup(self, type):
        self.type = type

    def postAPI(self, controller, parameter, postData):
        try:
            entity = validator.retrieve(postData, self.type)
            # remove entity from database
            entity.key.delete()
            return '{"success": 1}'
        except Exception as e:
            raise e


class ModelUpdateHandler(VerbHandler):

    def __init__(self, view = None):
        super(ModelUpdateHandler, self).__init__(view)

    def setup(self, type):
        self.type = type

    def postAPI(self, controller, parameter, postData):
        try:
            entity = validator.update(postData, self.type)
            entity.put()
            return '{"success": 1}'
        except Exception as e:
            raise e

