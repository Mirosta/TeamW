from payme.controller.modelHandler import ModelHandler, RelatedModel, ReadOnlyFunction
from payme.model.group import Group

class NotificationHandler(ModelHandler):

    def __init__(self):
        super(NotificationHandler, self).__init__(None, {}, 'getNotification', User, [], [])