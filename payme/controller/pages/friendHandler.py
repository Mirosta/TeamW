from payme.controller.contentHandler import PageHandler, Parameter
from payme.model.user import User

class FriendHandler(PageHandler):

    # dummy for currentUser
    currentUser = User.query(User.googleID == 'john').fetch(10)[0]

    def __init__(self):
        super(FriendHandler, self).__init__('friends', Parameter(Parameter.Type.Int, False, True))

    def postAPI(self, controller, parameter):
        return '{error: "Not yet implemented"}'

    def getAPI(self, controller, parameter):
        if parameter == Parameter.NoneGiven:
            return self.outputAllFriends()
        if parameter == Parameter.Invalid:
            return self.onInvalidFriends()
        if int(parameter) != 1:
            return self.onUnknownFriend()
        return self.displayGroup()

    def getAllFriends(self):

        friendKeys = self.currentUser.getFriends()
        friends = []

        for key in friendKeys:
            friends.append(User.query(User.key == key).fetch(10)[0])

        return friends

    def outputAllFriends(self):
        return self.serialize(self.getAllFriends())

    def displayFriend(self, userKey):

        friendKeys = self.currentUser.getFriends()
        found = False

        for key in friendKeys:
            if userKey == key:
                found = True

        if found:
            return User.query(User.key == userKey).fetch(10)[0]
        else:
            return '{error: "Friend not found"}'

        # return '{error: "Not yet implemented"}' #'{"name": "TestGroup", "id": 1, "users": [{"name": "TestUser", "id": 1},{"name": "TestUser2", "id": 2}]}'

    def onInvalidParameter(self):
        return '{error: "Invalid argument"}'
    def onUnknownFriend(self):
        return '{error: "No friend with that ID"}'