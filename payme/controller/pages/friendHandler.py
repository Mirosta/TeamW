from google.appengine.ext.ndb import Key
from payme.controller import validator
from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.model.user import User
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction, ModelAddHandler, \
    ModelRemoveHandler
import json


class FriendHandler(ModelHandler):

    def __init__(self):
        super(FriendHandler, self).__init__('friends',
                                            {'add' : FriendHandler.AddHandler(),
                                             'request': FriendHandler.RequestHandler(self),
                                             'remove': FriendHandler.RemoveHandler()},
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
                if json_obj.get('email') is not None:
                    user = User.query(User.email == json_obj['email']).fetch(1)
                elif json_obj.get('key') is not None:
                    user = User.query(User.key == Key(urlsafe=json_obj['key'])).fetch(1)
                if not user:
                    raise Exception()
                user = user[0]
                controller.getCurrentUser().addFriend(user.key)
                return '{"success": 1}'
            except Exception as e:
                raise e


    class RemoveHandler(ModelRemoveHandler):

        def postAPI(self, controller, parameter, postData):
            try:
                friend = validator.retrieve(postData, self.type)
                controller.getCurrentUser().removeFriend(friend.key)
                return '{"success": 1}'
            except Exception as e:
                raise e
