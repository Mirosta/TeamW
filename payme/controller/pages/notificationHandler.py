from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction
from payme.model.notification import Notification

from payme.model.group import Group

class NotificationHandler(ModelHandler):

    def __init__(self):
        super(NotificationHandler, self).__init__(None, {}, 'getNotifications', Notification, [], [])