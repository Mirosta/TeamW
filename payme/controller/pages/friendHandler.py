from payme.controller import validator
from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.model.user import User
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction, ModelAddHandler
import json


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

    class AddHandler(ModelAddHandler):

        def postAPI(self, controller, parameter, postData):
            try:
                json_obj = json.loads(postData)
                controller.getCurrentUser().addFriend(User.query(User.email == json_obj['email']).fetch(1)[0].key)
                return '{"success": 1}'
            except Exception as e:
                raise e