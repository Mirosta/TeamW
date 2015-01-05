from payme.controller import validator
from payme.controller.contentHandler import PageHandler, Parameter, VerbHandler
from payme.model.user import User
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction, ModelAddHandler, ModelUpdateHandler, \
ModelRemoveHandler
from payme.model.group import Group

class GroupHandler(ModelHandler):

    def __init__(self):
        # super(GroupHandler, self).__init__('groups', Parameter(Parameter.Type.Int, False, True))
        super(GroupHandler, self).__init__("groups",
                                           {'add': AddHandler(),
                                            'update': ModelUpdateHandler(),
                                            'remove': RemoveHandler()},
                                           'getGroups', Group, [],
                                           [ReadOnlyFunction('getNetAmount', 'netAmount'),
                                            ReadOnlyFunction('getCreditAmount', 'Own'),
                                            ReadOnlyFunction('getDebtAmount', 'Owe')])


    def postAPI(self, controller, parameter, postData):
        return '{error: "Not yet implemented"}'

    # def getAPI(self, controller, parameter):
    #     if parameter == Parameter.NoneGiven:
    #         return self.outputAllGroups()
    #     if parameter == Parameter.Invalid:
    #         return self.onInvalidParameter()
    #     if int(parameter) != 1:
    #         return self.onUnknownGroup()
    #     return self.displayGroup()

    # Output all group I belong to
    def outputAllGroups(self):
        # return self.serialize()
        return '{"results": [' + self.displayGroup() + ']}'

    # def queryGroup(self):

    def displayGroup(self):
        return '{"name": "TestGroup", "id": 1, "users": [{"name": "TestUser", "id": 1},{"name": "TestUser2", "id": 2}], "readonly": {"netAmount": 1337}}'

    def onInvalidParameter(self):
        return '{error: "Invalid group ID"}'
    def onUnknownGroup(self):
        return '{error: "No group with that ID"}'


class AddHandler(ModelAddHandler):

    def postAPI(self, controller, parameter, postData):
        try:
            group = validator.create(postData, self.type)
            # add new entity to database
            group.put()
            controller.getCurrentUser().addGroup(group.key)
            return '{"success": 1}'
        except Exception as e:
            raise e

class RemoveHandler(ModelRemoveHandler):

    def __init__(self):
        super(RemoveHandler, self).__init__('remove')

    def postAPI(self, controller, parameter, postData):
        try:
            group = validator.retrieve(postData, self.type)
            # remove entity from database
            group.removeMe()
            group.key.delete()
            return '{"success": 1}'
        except Exception as e:
            raise e
