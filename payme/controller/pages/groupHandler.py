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
                                           {'add': ModelAddHandler(),
                                            'update': ModelUpdateHandler(),
                                            'remove': ModelRemoveHandler()},
                                           'getGroups', Group, [],
                                           [ReadOnlyFunction('getNetAmount', 'netAmount'),
                                            ReadOnlyFunction('getCreditAmount', 'Own'),
                                            ReadOnlyFunction('getDebtAmount', 'Owe')])

class RemoveHandler(ModelRemoveHandler):

    def __init__(self):
        super(RemoveHandler, self).__init__('remove')

    def postAPI(self, controller, parameter, postData):
        group = validator.retrieve(postData, self.type)
        group.removeMe()
        return '{"success": 1}'