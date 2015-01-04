from payme.controller.exceptions import InvalidParameterError, MissingFieldError
import json
from google.appengine.ext.ndb import Key

all_required = []
create_debt_required = ['debtor', 'creditor', 'amount', 'description', 'isPaid', 'created', 'amountPaid']
retrieve_required = ['key']


def create(json_str, type_class, required_fields=[]):
    required_fields.extend(all_required)
    try:
        json_obj = json.loads(json_str)
        for key in required_fields:
            if key not in json_obj:
                raise MissingFieldError()
        return type_class(**json_obj)
    except:
        raise InvalidParameterError()


def retrieve(json_str, type_class, required_fields=[]):
    required_fields.extend(all_required)
    required_fields.extend(retrieve_required)
    try:
        json_obj = json.loads(json_str)
        for key in required_fields:
            if key not in json_obj:
                raise MissingFieldError()
        return type_class.query(type_class.key == Key(urlsafe=json_obj.get('key'))).fetch(1)[0]
    except Exception as e:
        raise e