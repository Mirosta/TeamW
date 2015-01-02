from payme.controller.contentHandler import PageHandler, Parameter

class FriendHandler(PageHandler):
    def __init__(self):
        super(FriendHandler, self).__init__('friends', Parameter(Parameter.Type.Int, False, True))

    def postAPI(self, controller, parameter):
        return '{error: "Not yet implemented"}'

    def getAPI(self, controller, parameter):
        if parameter == Parameter.NoneGiven:
            return self.outputAllGroups()
        if parameter == Parameter.Invalid:
            return self.onInvalidParameter()
        if int(parameter) != 1:
            return self.onUnknownGroup()
        return self.displayGroup()

    def outputAllFriends(self):
        return '{error: "Not yet implemented"}'#'{"results": [' + self.displayGroup() + ']}'

    def displayFriend(self):
        return '{error: "Not yet implemented"}' #'{"name": "TestGroup", "id": 1, "users": [{"name": "TestUser", "id": 1},{"name": "TestUser2", "id": 2}]}'

    def onInvalidParameter(self):
        return '{error: "Invalid friend ID"}'
    def onUnknownFriend(self):
        return '{error: "No friend with that ID"}'