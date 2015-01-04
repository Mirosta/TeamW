from payme.controller.exceptions import InvalidParameterError, MissingFieldError
import json

all_required = []


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
    try:
        json_obj = json.loads(json_str)
        for key in required_fields:
            if key not in json_obj:
                raise MissingFieldError()
        return type_class.query(type_class.key == json_obj[key]).fetch(1)[0]
    except:
        raise InvalidParameterError()