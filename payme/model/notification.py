from google.appengine.ext import ndb

class Notification(ndb.Model):
    'A Notification object is used to store (for display) information following a user action'

    # Type of notification, i.e. info, error, success (blue, red, green?)
    type = ndb.StringProperty()
    content = ndb.StringProperty()

    # possibly unnecessary, useful for setting type neatly?
    class Type:
        INFO = "INFO"
        ERROR = "ERROR"
        SUCCESS = "SUCCESS"
        MISC = "MISC"

    def getType(self):
        return self.type

    def getContent(self):
        return self.content

    def setType(self, notificationType):
        self.type = notificationType

    def setContent(self, contentString):
        self.content = contentString