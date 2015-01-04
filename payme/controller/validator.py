from payme.controller.exceptions import InvalidParameterError, MissingFieldError
import json


def validate(json_str, type_class, required_fields=()):
    try:
        json_obj = json.loads(json_str)
        for key in required_fields:
            if key not in json_obj:
                raise MissingFieldError()
        return type_class(**json_obj)
    except:
        raise InvalidParameterError()