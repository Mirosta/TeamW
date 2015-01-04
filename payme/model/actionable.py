from payme.controller.exceptions import AttributeNotFound, UpdateNotAllowed
from entity import Entity
import logging

from google.appengine.ext import ndb

class Actionable(ndb.Model):

    notUpdatableAttributes = []

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

# to update debt        validate    creditor
#           payment                 debtor
#           user attrs              user (that is the user)
#           group                   group is include in user's group list
