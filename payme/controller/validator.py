from google.appengine.api.datastore_errors import BadValueError
from payme.controller.exceptions import InvalidParameterError, MissingFieldError


def validate(json_obj, type_class, required_fields=()):
    try:
        for key in required_fields:
            if key not in json_obj:
                raise MissingFieldError()
        return type_class(**json_obj)
    except (MissingFieldError, BadValueError, AttributeError):
        raise InvalidParameterError()