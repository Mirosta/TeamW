from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter
from payme.model.user import User
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction

class FriendHandler(ModelHandler):

    # dummy for currentUser
    # currentUser = User.query(User.googleID == 'john').fetch(10)[0]

    def __init__(self):
        super(FriendHandler, self).__init__('friends', {'add' : FriendHandler.AddHandler()}, 'getFriends', User, [], [ReadOnlyFunction('getOE', 'netAmount')])
        # super(FriendHandler, self).__init__('friends', Parameter(Parameter.Type.Int, False, True))

    def postAPI(self, controller, parameter):
        return '{error: "Not yet implemented"}'

    # def getAPI(self, controller, parameter):
    #     # if parameter == Parameter.NoneGiven:
    #     #     return self.outputAllFriends()
    #     if parameter == Parameter.Invalid:
    #         return self.onInvalidFriends()
    #     # if int(parameter) != 1:
    #     #     return self.onUnknownFriend()
    #     return self.displayFriend(parameter)

    def getAllFriends(self):

        friendKeys = self.currentUser.getFriends()
        friends = []

        for key in friendKeys:
            user = User.query(User.key == key).fetch(10)[0]
            data = user.to_dict()
            data['readOnly'] = {'netAmount': user.getOE(), 'Owe': user.getCR(), 'Own': user.getDR()}

            friends.append(data)

        return friends

    def outputAllFriends(self):
        return self.serialize({'results': self.getAllFriends()})

    def displayFriend(self, userKey):

        friendKeys = self.currentUser.getFriends()
        found = False

        for key in friendKeys:
            if userKey == key:
                found = True

        if found:
            return self.queryUser(userKey)
        else:
            return '{error: "Friend not found"}'

    def onInvalidParameter(self):
        return '{error: "Invalid argument"}'
    def onUnknownFriend(self):
        return '{error: "No friend with that ID"}'


    class AddHandler(VerbHandler):

        def __init__(self):
            super(FriendHandler.AddHandler, self).__init__('addFriend')
            self.parameter = Parameter(Parameter.Type.NoParameter, False, False)