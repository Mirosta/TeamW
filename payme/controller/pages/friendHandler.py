from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.model.user import User
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction, ModelAddHandler


class FriendHandler(ModelHandler):

    def __init__(self):
        super(FriendHandler, self).__init__('friends',
                                            {'add' : FriendHandler.AddHandler(),
                                             'request': FriendHandler.RequestHandler(self)},
                                            'getFriends', User, [],
                                            [ReadOnlyFunction('getOE', 'netAmount'),
                                             ReadOnlyFunction('getDRKeys', 'debts'),
                                             ReadOnlyFunction('getCRKeys', 'credits')],
                                            ['credentials', 'friends', 'groups', 'messageQueue'])

    class AddHandler(ModelAddHandler):

        def __init__(self):
            super(FriendHandler.AddHandler, self).__init__('addFriend')
            self.parameter = Parameter(Parameter.Type.NoParameter, False, False)

    class RequestHandler(VerbHandler):

        def __init__(self, modelHandler):
            super(FriendHandler.RequestHandler, self).__init__('requestFriend')
            self.modelHandler = modelHandler

        def getAPI(self, controller, parameter):
            return self.getRequests(controller)

        def getRequests(self, controller):
            models = controller.getCurrentUser().getFriendRequests()
            results = []
            for model in models:
                results.append(self.modelHandler.getOneInner(controller, model))
            return self.modelHandler.serialize({'results': results})

