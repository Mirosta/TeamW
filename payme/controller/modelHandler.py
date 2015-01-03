import json
from payme.controller.contentHandler import PageHandler
from datetime import date, datetime

class ModelHandler(PageHandler):
    def serialize(self, object_to_serialize):
        return json.dumps(object_to_serialize, cls=JSonAPIEncoder)



class JSonAPIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return obj.strftime('%Y/%m/%d %H:%M:%S')
        elif isinstance(obj, ndb.Model):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)

