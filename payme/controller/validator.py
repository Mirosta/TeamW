
class Validator:

    required_fields = {'debt': [], 'entity': [], 'group': [], 'payment': [], 'user': []}
    field_types = {'debt': {'description': basestring}}

    def __init__(self):
        pass

    def parse(self, json_obj, type):
        if type in Validator.required_fields:
            # Validate json object contains the required field for its type
            for key in Validator.required_fields[type]:
                if key not in json_obj:
                    raise MissingField(key)

            # Validate every field the json object contains is of the correct type
            for key in json_obj:
                if not isinstance(key, Validator.field_types[type][key]):
                    raise IncorrectType('%s. Required type: %s' % (key, Validator.field_types[type][key]))

            return json_obj
        else:
            raise UndefinedType(type)


class MissingField(Exception):
    pass


class IncorrectType(Exception):
    pass


class UndefinedType(Exception):
    pass