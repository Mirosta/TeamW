import json
from google.appengine.ext.ndb import Key
from google.appengine.ext import ndb
from payme.model.debt import Debt
from payme.model.group import Group
from payme.model.payment import Payment
from globals import Global
import time


all_required = []
required_fields = {
    Debt: ['debtor', 'creditor', 'amount', 'description', 'isPaid', 'created', 'amountPaid'],
    Group: ['name', ],
    Payment: ['payer', 'debt', 'amount', 'created', 'description']
}

json_convert = {
    ndb.DateTimeProperty: lambda x: time.strptime(x, Global.JSONDateTime),
    ndb.KeyProperty: lambda x: Key(urlsafe=x)
}


def create(json_str, type_class):
    json_obj = json.loads(json_str)
    entity = type_class()
    set_attributes(entity, json_obj, type_class)
    return entity


def retrieve(json_str, type_class, key_id = None):
    if key_id is None:
        key_id = json.loads(json_str)['key']
    results = type_class.query(type_class.key == Key(urlsafe=key_id)).fetch(1)
    if len(results) < 1:
        return None
    return results[0]


def update(json_str, type_class):
    json_obj = json.loads(json_str)
    entity = retrieve(json_str, type_class, json_obj['key'])
    if entity is None:
        return None
    del json_obj['key']
    set_attributes(entity, json_obj, type_class)
    return entity


def set_attributes(entity, json_obj, type_class):
    for key, value in json_obj.iteritems():
        convert = json_convert.get(type(type_class._properties[key]))
        if convert is not None:
            setattr(entity, key, convert(value))
        else:
            setattr(entity, key, value)