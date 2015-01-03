import json
import logging
from google.appengine.ext import ndb
from google.appengine.ext.ndb import Key
from payme.controller.contentHandler import PageHandler, Parameter
from datetime import date, datetime
import sys
import types
from payme.model.user import User


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

    def __init__(self, view, verbs, getAllFunction, modelClass, relatedModels = [], readOnlyFunctions = []):
        super(ModelHandler, self).__init__(view, Parameter(Parameter.Type.String), verbs)
        self.getAllFunction = getAllFunction
        self.modelClass = modelClass
        self.relatedModels = relatedModels#[RelatedModel('Payment', 'debt')]
        self.readOnlyFunctions = readOnlyFunctions #example: [ReadOnlyFunction('getOE','netAmount'), ReadOnlyFunction('getCR','Owe'), ReadOnlyFunction('getDR', 'Own')]

    #Called by the controller when someone visits a /api/ link
    def getAPI(self, controller, parameter):
        if parameter == Parameter.NoneGiven: #If no parameter is given, assume they want all
            return self.getAll(controller)
        if parameter == Parameter.Invalid:
            return self.onInvalidParameter() # change
        # if int(parameter) != 1:
        #     return self.onUnknownFriend() # change
        return self.getOne(controller, parameter) #If a parameter is given and is valid, lookup by the key given

    #Gets all models
    def getAll(self, controller):
        currentUser = User.query(User.googleID == 'john').fetch()[0] # controller.getCurrentUser()
        function = getattr(currentUser, self.getAllFunction)
        logging.info('Get all function:')
        logging.info(function)
        models = function()
        modelsOutput = []

        for model in models:
            data = self.getOneInner(controller, model)

            modelsOutput.append(data)

        return self.serialize({'results': modelsOutput})

    def getOne(self, controller, parameter):
        models = self.modelClass.query(self.modelClass.key == Key(urlsafe=parameter)).fetch()
        if models.__len__() < 1:
            return self.onModelNotFound()
        data = self.getOneInner(controller, models[0])
        return self.serialize(data)

    def getOneInner(self, controller, model):
        data = model.to_dict()
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
        return json.dumps(object_to_serialize, cls=self.JSonAPIEncoder)

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