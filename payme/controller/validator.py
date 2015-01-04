from google.appengine.api.datastore_errors import BadValueError
from payme.controller.exceptions import InvalidParameterError, MissingFieldError
import json
from payme.model.debt import Debt
from payme.model.group import Group
from payme.model.payment import Payment
from payme.model.user import User


class Validator:

    def __init__(self):
        pass

    def validate(self, json_str, type_class, required_fields = []):
        json_obj = json.loads(json_str)
        entity = type_class()
        try:
            for key in required_fields:
                if key not in json_obj:
                    raise MissingFieldError()
            for key, value in json_obj.iteritems():
                if key not in type_class._properties:
                    raise MissingFieldError()
                setattr(entity, key, value)
            return entity
        except:
            raise InvalidParameterError()


if __name__ == '__main__':
    validator = Validator()
    validator.validate('''
    {
        "amount": 1,
        "description": "test"
    }
    ''', Debt, [])

