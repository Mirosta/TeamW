from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.model.user import User
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction, ModelAddHandler


class FriendHandler(ModelHandler):

    def __init__(self):
        super(FriendHandler, self).__init__('friends',
                                            {'add' : FriendHandler.AddHandler()},
                                            'getFriends', User, [],
                                            [ReadOnlyFunction('getOE', 'netAmount'),
                                             ReadOnlyFunction('getDRKeys', 'debts'),
                                             ReadOnlyFunction('getCRKeys', 'credits')],
                                            ['credentials', 'friends', 'groups', 'messageQueue'])

    class AddHandler(ModelAddHandler):

        def __init__(self):
            super(FriendHandler.AddHandler, self).__init__('addFriend')
            self.parameter = Parameter(Parameter.Type.NoParameter, False, False)
