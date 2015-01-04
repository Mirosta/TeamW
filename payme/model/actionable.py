from payme.controller.exceptions import AttributeNotFound, UpdateNotAllowed
from entity import Entity
import logging

from google.appengine.ext import ndb

class Actionable(ndb.Model):

    # Attributes of the model classes. To be overridden to
    # specify which attributes in the model cannot be updated/changed
    notUpdatableAttributes = []

    # A generic update method that takes a map of attr_name -> value.
    # Checks against the notUpdatableAttributes list above.
    def update(self, values):

        if self.isUpdateAllowed():
            for key, value in values.iteritems():
                try:
                    if key in self.notUpdatableAttributes:
                        raise UpdateNotAllowed()
                    else:
                        setattr(self, key, value)

                except AttributeError:
                    raise AttributeNotFound()

            self.put()
        else:
            raise UpdateNotAllowed()

    # Methods to override in each model class if not True by default
    def isRemoveAllowed(self):
        return True

    def isUpdateAllowed(self):
        return True

    def isAddAllowed(self):
        return True
