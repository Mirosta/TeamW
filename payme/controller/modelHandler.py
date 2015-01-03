import json
from google.appengine.ext import ndb
from google.appengine.ext.ndb import Key
from payme.controller.contentHandler import PageHandler
from datetime import date, datetime
import sys
import types

class RelatedModel:

    def __init__(self, modelName, referencingModelField, jsonFieldName):
        self.modelName = modelName
        self.referencingModelField = referencingModelField
        self.jsonFieldName = jsonFieldName
        self.resolvedClass = None

    def getModelField(self):
        getattr(self.getClass(), self.referencingModelField)

    def getClass(self):
        if self.resolvedClass is None:
            self.resolvedClass = self.strToClass(self.modelName)
        return self.resolvedClass

class ReadOnlyFunction:

    def __init__(self, functionName, jsonFieldName):
        self.functionName = functionName
        self.jsonFieldName = jsonFieldName

    #http://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
    def strToClass(field):
        try:
            identifier = getattr(sys.modules[__name__], field)
        except AttributeError:
            raise NameError("%s doesn't exist." % field)
        if isinstance(identifier, (types.ClassType, types.TypeType)):
            return identifier
        raise TypeError("%s is not a class." % field)

class ModelHandler(PageHandler):

    def __init__(self, view, verbs, getAllFunction, modelClass, relatedModels = [], readOnlyFunctions = []):
        super(ModelHandler, self).__init__(view, Parameter(Parameter.Type.String), verbs)
        self.getAllFunction = getAllFunction
        self.modelClass = modelClass
        self.relatedModels = relatedModels#[RelatedModel('Payment', 'debt')]
        self.readOnlyFunctions = readOnlyFunctions #example: [ReadOnlyFunction('getOE','netAmount'), ReadOnlyFunction('getCR','Owe'), ReadOnlyFunction('getDR', 'Own')]

    def serialize(self, object_to_serialize):
        return json.dumps(object_to_serialize, cls=JSonAPIEncoder)

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
        currentUser = controller.getCurrentUser()
        function = getattr(currentUser, self.getAllFunction)
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
            relatedValues = relatedModel.getClass().query(relatedModel.getModelField() == model.key)
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

class JSonAPIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return obj.strftime('%Y/%m/%d %H:%M:%S')
        elif isinstance(obj, ndb.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)


from payme.controller.contentHandler import PageHandler, Parameter, VerbHandler
from payme.model.debt import Debt
from payme.model.user import User
from payme.model.payment import Payment

class DebtHandler(PageHandler):

    # dummy for currentUser
    #currentUser = User.query(User.googleID == 'john').fetch(10)[0]

    def __init__(self):
        super(DebtHandler, self).__init__(None, Parameter(Parameter.Type.String), {})

    def getAPI(self, controller, parameter):
        if parameter == Parameter.NoneGiven:
            return self.displayAllDebt()
        if parameter == Parameter.Invalid:
            return self.onInvalidParameter() # change
        # if int(parameter) != 1:
        #     return self.onUnknownFriend() # change
        return self.displayDebtOweTo(parameter)

    # returns all debt owed by that user - CHECKED
    def displayAllDebt(self):

        debts = self.currentUser.getCRs()
        debtsOutput = []

        for debt in debts:
            data = debt.to_dict()

            payments = Payment.query(Payment.debt == debt.key)
            paymentOutput = []

            for payment in payments:
                paymentOutput.append(payment.key)

            data['readOnly'] = {'payments': paymentOutput}

            debtsOutput.append(data)

        return self.serialize({'results': debtsOutput})

    # returns all debt owed by that user to a specified creditor - CHECKED
    def displayDebtOweTo(self, key):
        return self.serialize(Debt.query(Debt.debtor == self.currentUser.key, Debt.creditor == self.queryUserByID(key).key).fetch(10))

    # debug - helper for function above
    def queryUserByID(self, googleID):
        return User.query(User.googleID == googleID).fetch(10)[0]

    def onInvalidParameter(self):
        return '{error: "Invalid debt key"}'

    # Not sure about this...
    # def onUnknownFriend(self):
    #     return '{error: "No friend with that ID"}'