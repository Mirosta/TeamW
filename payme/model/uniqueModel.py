import logging
from google.appengine.ext import ndb

class HasUniqueProperty(ndb.Model):
    uniqueProperty = None
    def put(self):
        uniqueProperty = getattr(self, 'uniqueProperty')
        updateKey = None
        if uniqueProperty != None:
            scopeName = '%s.%s' % (self.__class__.__name__, uniqueProperty)
            if not hasattr(self, uniqueProperty): raise UniqueConstraintError('Unknown property ' + uniqueProperty)
            updateKey = Unique.check(scopeName, getattr(self, uniqueProperty), self.key)
            if not self.key is None: updateKey = None

        newKey = super(HasUniqueProperty, self).put()
        logging.info('update key after check is ' + 'None' if updateKey is None else updateKey.id().__str__())
        if not updateKey is None:
            toUpdate = updateKey.get()
            toUpdate.modelKey = newKey
            toUpdate.put()
            logging.info('Updated ' + updateKey.id().__str__() + ' with modelKey ' + newKey.id().__str__())

        return newKey


#http://squeeville.com/2009/01/30/add-a-unique-constraint-to-google-app-engine/
class Unique(ndb.Model):
    modelKey = ndb.KeyProperty(indexed=True)

    @classmethod
    def check(cls, scope, value, key):

        needToDelete = [False]
        key_name = "U%s:%s" % (scope, value)

        @ndb.transactional(retries=3)
        def tx(scope, value, key):
            logging.info('Checking uniqueness for key with name ' + key_name)
            logging.info('Key ID: ' + ('None' if key is None else key.id().__str__()))
            ue = Unique.get_by_id(key_name)

            if ue and (key is None or ue.modelKey.id() != key.id()): raise UniqueConstraintViolation(scope, value)
            if not key is None and not ue:
                needToDelete[0] = True

            ue = Unique(id=key_name, modelKey = key)
            updateKey = ue.put()
            logging.info('Transaction done')
            return updateKey

        updateKey = tx(scope, value, key)
        logging.info('After transaction')
        logging.info('Update key ' + updateKey.id().__str__())
        if needToDelete[0]:
            logging.info('Need to delete old key')
            all = Unique.query(Unique.modelKey == key).fetch(2)
            for ue in all:
                logging.info('Found unique with id ' + ue.key.id().__str__())
                if not ue.key.id() == key_name:
                    ue.key.delete()
                    break
        return updateKey

class UniqueConstraintError(Exception):
    pass
class UniqueConstraintViolation(Exception):
  def __init__(self, scope, value):
    super(UniqueConstraintViolation, self).__init__("Value '%s' is not unique within scope '%s'." % (value, scope))