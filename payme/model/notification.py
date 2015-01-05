from google.appengine.ext import ndb
from actionable import Actionable

class Notification(Actionable):
    'A Notification object is used to store (for display) information following a user action'

    # Type of notification, i.e. info, error, success, misc, friend request
    type = ndb.StringProperty()

    content = ndb.StringProperty()

    # Whether the notification has been seen by the user yet, obviously false by default
    seen = ndb.BooleanProperty(default=False)

    class Type:
        INFO = "INFO"
        ERROR = "ERROR"
        SUCCESS = "SUCCESS"
        MISC = "MISC"
        FRIEND_REQUEST = "FRIEND_REQUEST"

    def getType(self):
        return self.type

    def getContent(self):
        return self.content

    def setType(self, notificationType):
        self.type = notificationType

    def setContent(self, contentString):
        self.content = contentString