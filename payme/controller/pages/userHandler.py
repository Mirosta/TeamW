from payme.controller.contentHandler import ContentHandler, Parameter, VerbHandler, PageHandler
from payme.controller.exceptions import UnsupportedMethod
from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction
import logging

from payme.model.user import User

class UserHandler(ModelHandler):

    def __init__(self):
        # super(UserHandler, self).__init__(None, Parameter(Parameter.Type.String), {'login': UserHandler.LoginHandler(), 'profile' : UserHandler.ProfileHandler()}) #This page has no view, but it does have verbs
        super(UserHandler, self).__init__(None, {'login': UserHandler.LoginHandler(),
                                                 'logout': UserHandler.LogoutHandler(),
                                                 'profile': UserHandler.ProfileHandler(),
                                                 'redirect': UserHandler.RedirectHandler()},
                                          'getMe',
                                          User, [],
                                          [ReadOnlyFunction('getOE', 'netWorth'),
                                           ReadOnlyFunction('getCR', 'debt'),
                                           ReadOnlyFunction('getDR', 'credit')],
                                          ['credentials'])

    def getOne(self, controller, parameter):
        raise UnsupportedMethod

    class LoginHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.LoginHandler, self).__init__('login')
            self.accessLevel = 0

        def getHTML(self, controller, parameter):
            if not controller.getCurrentUser() is None:
                controller.redirect(controller.homePage)
                return
            return super(UserHandler.LoginHandler, self).getHTML(controller, parameter)

    class RedirectHandler(VerbHandler):
        def __init__(self):
            super(UserHandler.RedirectHandler, self).__init__(None)

        def getHTML(self, controller, parameter):
            if controller.session.has_key('redirectTo'):
                logging.info("Session has redirect:")
                logging.info(controller.session['redirectTo'])
                redirect = controller.homePage#controller.session['redirectTo']
            else:
                redirect = controller.homePage
            controller.redirect(redirect)
            return


    class LogoutHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.LogoutHandler, self).__init__('logout')

        def getHTML(self, controller, parameter):
            controller.session.clear()
            controller.redirect(controller.loginPage)
            return

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




