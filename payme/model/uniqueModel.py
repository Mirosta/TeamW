from google.appengine.ext import ndb

class HasUniqueProperty(ndb.Model):
    uniqueProperty = None
    def put(self):
        uniqueProperty = getattr(self, 'uniqueProperty')
        if uniqueProperty != None:
            scopeName = '%s.%s' % (self.__class__.__name__, uniqueProperty)
            if not hasattr(self, uniqueProperty): raise UniqueConstraintError('Unknown property ' + uniqueProperty)
            Unique.check(scopeName, getattr(self, uniqueProperty))
        super(HasUniqueProperty, self).put()


#http://squeeville.com/2009/01/30/add-a-unique-constraint-to-google-app-engine/
class Unique(ndb.Model):
    @classmethod
    def check(cls, scope, value):
        @ndb.transactional(retries=3)
        def tx(scope, value):
            key_name = "U%s:%s" % (scope, value)
            ue = Unique.get_by_id(key_name)

            if ue: raise UniqueConstraintViolation(scope, value)
            ue = Unique(id=key_name)
            ue.put()

        tx(scope, value)

class UniqueConstraintError(Exception):
    pass
class UniqueConstraintViolation(Exception):
  def __init__(self, scope, value):
    super(UniqueConstraintViolation, self).__init__("Value '%s' is not unique within scope '%s'." % (value, scope))