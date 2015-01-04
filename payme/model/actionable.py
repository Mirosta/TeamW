from payme.controller.exceptions import AttributeNotFound, UpdateNotAllowed
from entity import Entity
import logging

from google.appengine.ext import ndb

class Actionable(ndb.Model):

    notUpdatableAttributes = ['amount', 'created', 'uniqueProperty', 'googleID', 'payer', 'debt', 'creditor', 'debtor', 'content', 'type']

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

    def isUpdateAllowed(self): # override me
        return True

    def isAddAllowed(self):
        return True

# to update debt        validate    creditor
#           payment                 debtor
#           user attrs              user (that is the user)
#           group                   group is include in user's group list
