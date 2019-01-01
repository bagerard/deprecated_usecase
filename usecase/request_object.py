import formencode as fe


class DynamicFeSchema(fe.Schema):
    """Dynamic implementation of formencode.Schema
    It allows to create a Schema class from a constructor i.o using the class attributes
    which allow schemas to be created on the fly
    """
    allow_extra_fields = False

    def __init__(self, chained_validators=(), **validators):
        super(DynamicFeSchema, self).__init__()
        for k, v in validators.items():
            self.add_field(k, v)
        self.chained_validators = chained_validators


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
        parser = DynamicFeSchema(
            **cls._fields_validators,
            **cls._validators_options,
        )
        res = parser.to_python(dict_)
        return cls(**res)



