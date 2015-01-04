from payme.controller.exceptions import InvalidParameterError, MissingFieldError
import json
from google.appengine.ext.ndb import Key
from google.appengine.ext import db
from google.appengine.ext import ndb
from payme.model.debt import Debt
from payme.model.group import Group
from payme.model.payment import Payment
from payme.model.user import User


all_required = ['key']
required_fields = \
{
    Debt: ['debtor', 'creditor', 'amount', 'description', 'isPaid', 'created', 'amountPaid'],
    Group: [],
    Payment: [],
    User: []
}


def create(json_str, type_class):
    json_obj = json.loads(json_str)
    for key in required_fields[type_class].extend(all_required):
        if key not in json_obj:
            raise MissingFieldError()
    return type_class(**json_obj)


def retrieve(json_str, type_class, key_id = None):
    if key_id is None:
        key_id = json.loads(json_str)['key']
    return type_class.query(type_class.key == Key(urlsafe=key_id)).fetch(1)[0]


def update(json_str, type_class):
    json_obj = json.loads(json_str)
    entity = retrieve(json_str, type_class, json_obj['key'])
    del json_obj['key']
    entity.populate(**json_obj)
    return entity