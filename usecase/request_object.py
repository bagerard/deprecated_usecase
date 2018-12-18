import json
from collections import namedtuple

import formencode as fe


class RequestArgParser(fe.Schema):
    """This is a dynamic implementation of formencode.Schema
    Given a dict, it will validate it against the formencode.validators
    provided in the constructor. In case validation(s) fails, it will raise an
    formencode.validators.Invalid exception with the details of the problem
    """
    allow_extra_fields = True
    filter_extra_fields = True

    def __init__(self, chained_validators=None, json_fields=None, if_missing=fe.NoDefault, **validators):
        super(RequestArgParser, self).__init__()
        self.if_missing = if_missing
        for k, v in validators.items():
            self.add_field(k, v)
        self.chained_validators = chained_validators or ()
        self.json_fields = json_fields or ()

    def _convert_to_python(self, value_dict, state=None):
        """return a namedtuple"""
        if not isinstance(value_dict, dict):
            raise fe.Invalid('Invalid value: expected an object but received {}'.format(type(value_dict)),
                             value_dict, state)
        value_dict = self._clean_dict(value_dict, state)
        res_dic = super(RequestArgParser, self)._convert_to_python(value_dict, state)
        if res_dic is None:
            return res_dic
        keys, vals = list(zip(*res_dic.items()))
        return namedtuple('RequestObj', keys)(*vals)

    def _clean_dict(self, value_dict, state=None):
        clean_dict = {}
        for key, value in value_dict.items():
            try:
                value = json.loads(value) if key in self.json_fields else value
            except (ValueError, TypeError):
                raise fe.Invalid('Invalid JSON for key [{}]: [{}]'.format(key, value),
                                 value_dict, state)
            clean_dict[key] = value
        return clean_dict


class FieldValidator:
    """Descriptor that exposes the validator instance as class attribute
    but the actual value when called from an instance
    """

    def __init__(self, validator):
        """
        :param validator: a validator
        :type validator: fe.validator
        """
        self.value = None
        self.validator = validator

    def __get__(self, instance, owner):
        if instance is None:
            # Document class being used rather than a document instance
            return self.validator
        return self.value

    def __set__(self, instance, value):
        self.value = value


class RequestObjectMeta(type):
    def __new__(mcls, name, bases, attrs):
        new_attrs = mcls.collect_new_attrs(attrs)
        return super(RequestObjectMeta, mcls).__new__(mcls, name, bases, new_attrs)

    @staticmethod
    def collect_new_attrs(attrs):
        """Turn fe.validators into FieldValidator and collect the fields"""
        new_attrs = {}
        fields_validators = {}
        validators_options = {}
        for attr_name, attr in attrs.items():
            if isinstance(attr, fe.FancyValidator):
                new_attrs[attr_name] = FieldValidator(attr)
                fields_validators[attr_name] = attr
            else:
                if attr_name in ('chained_validators', 'json_fields'):
                    validators_options[attr_name] = attr
                new_attrs[attr_name] = attr

        new_attrs['_fields_validators'] = fields_validators
        new_attrs['_validators_options'] = validators_options
        return new_attrs


class UseCaseRequestObject(object, metaclass=RequestObjectMeta):

    def __init__(self, **values):
        expected_fields = set(self._fields_validators)

        init_fields = set(values.keys())
        if init_fields != expected_fields:
            too_much = init_fields - expected_fields
            missing = expected_fields - init_fields
            raise ValueError(f"All RequestObject must be provided:\n{too_much}\n{missing}")

        for attr_name, attr_value in values.items():
            setattr(self, attr_name, attr_value)

    @classmethod
    def from_dict(cls, dict_):
        # if not dict_:
        #     return cls()
        parser = RequestArgParser(
            **cls._fields_validators,
            **cls._validators_options,
        )
        res = parser.to_python(dict_)
        return cls(**res._asdict())
