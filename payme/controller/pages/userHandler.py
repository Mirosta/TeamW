from payme.controller.contentHandler import ContentHandler, Parameter, VerbHandler, PageHandler
import json
from payme.model.user import User

class UserHandler(PageHandler):

    def __init__(self):
        super(UserHandler, self).__init__(None, Parameter(Parameter.Type.String), {'login': UserHandler.LoginHandler(), 'profile' : UserHandler.ProfileHandler()}) #This page has no view, but it does have verbs

    def getAPI(self, controller, parameter):

        # Dummy test, fetch by GoogleID
        user = User.query(User.googleID == parameter).fetch(10)

        if user.__len__() == 0:
            output = 'Not found'
        else:
            output = self.serialize(user[0])

        return output

        # Actual implementation below:
        # return self.serialize(self.queryUser(parameter))

    class LoginHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.LoginHandler, self).__init__('login')
            self.accessLevel = 0

        def getHTML(self, controller, parameter):
            return super(UserHandler.LoginHandler, self).getHTML(controller, parameter)

    class LogoutHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.LogoutHandler, self).__init__('logout')

        def getHTML(self, controller, parameter):
            return super(UserHandler.LogoutHandler, self).getHTML(controller, parameter)

    class ProfileHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.ProfileHandler, self).__init__('profile')

        def getHTML(self, controller, parameter):
            return super(UserHandler.ProfileHandler, self).getHTML(controller, parameter)

    class SettingsHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.SettingsHandler, self).__init__('settings')

        def getHTML(self, controller, parameter):
            return super(UserHandler.SettingsHandler, self).getHTML(controller, parameter)




