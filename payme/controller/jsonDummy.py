from payme.controller.contentHandler import PageHandler, VerbHandler, Parameter

class JSONDummy(PageHandler):

    def __init__(self):
        super(JSONDummy, self).__init__('lyuboTest', Parameter(Parameter.Type.Int, False, True))

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

    def outputAllGroups(self):
        return '{"results": [' + self.displayGroup() + ']}'

    def displayGroup(self):
        return '{"name": "TestGroup", "id": 1, "users": [{"name": "TestUser", "id": 1},{"name": "TestUser2", "id": 2}]}'

    def onInvalidParameter(self):
        return '{error: "Invalid group ID"}'
    def onUnknownGroup(self):
        return '{error: "No group with that ID"}'