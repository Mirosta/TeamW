from payme.controller.contentHandler import ContentHandler, Parameter, VerbHandler, PageHandler
import json
from datetime import date, datetime
from payme.model.user import User
from google.appengine.ext import ndb

class UserHandler(PageHandler):

    def __init__(self):
        super(UserHandler, self).__init__(None, Parameter(Parameter.Type.String), {'login': UserHandler.LoginHandler(), 'profile' : UserHandler.ProfileHandler()}) #This page has no view, but it does have verbs

    def serialize(self, object_to_serialize):
        return json.dumps(object_to_serialize, cls=JSonAPIEncoder)

    def getAPI(self, controller, parameter):

        user = User.query(User.googleID == 'john').fetch(10)[0]
        output = self.serialize(user)

        return output


    class LoginHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.LoginHandler, self).__init__('login')

        def getHTML(self, controller, parameter):
            return super(UserHandler.LoginHandler, self).getHTML(controller, parameter)

    class LogoutHandler(VerbHandler):

        def __init__(self):
            super(UserHandler.LogoutHandler, srelf).__init__('logout')

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



class JSonAPIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return obj.strftime('%Y/%m/%d %H:%M:%S')
        elif isinstance(obj, ndb.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)
