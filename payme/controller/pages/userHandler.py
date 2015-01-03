from payme.controller.contentHandler import ContentHandler, Parameter, VerbHandler, PageHandler

class UserHandler(PageHandler):

    def __init__(self):
        super(UserHandler, self).__init__(None, Parameter(Parameter.Type.String, ), {'login': UserHandler.LoginHandler(), 'logout': UserHandler.LogoutHandler(), 'profile': UserHandler.ProfileHandler, 'settings': UserHandler.SettingsHandler}) #This page has no view, but it does have verbs

    class LoginHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.LoginHandler, self).__init__('login')

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
