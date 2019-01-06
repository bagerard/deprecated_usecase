import formencode as fe
import pytest

from usecase.request_object import UseCaseRequestObject


class Human(UseCaseRequestObject):
    name = fe.validators.String(not_empty=True)
    age = fe.validators.Int(default=0)


class TestUseCaseRequestObject:
    def test____init____(self):
        human = Human(name='John', age=5)
        assert human.age == 5
        assert human.name == 'John'

    def test__descriptor__attr(self):
        assert isinstance(Human.age, fe.FancyValidator)

    def test____init____raises_when_additional_fields(self):
        with pytest.raises(ValueError, match="iq"):
            Human(name='John', age=5, iq=None)

    def test____init____raises_when_missing_fields(self):
        with pytest.raises(ValueError, match="age"):
            Human(name='John')

    def test__from_dict__validation_passes(self):
        Human.from_dict({'name': 'John', 'age': 5})

    def test__from_dict__validation_raises(self):
        with pytest.raises(fe.Invalid, match="age"):
            Human.from_dict({'name': 'John', 'age': [1, 2]})

    def test__from_dict__empty_dict_takes_default(self):
        class SampleRO(UseCaseRequestObject):
            name = fe.validators.String(if_missing='garbage')

        ro = SampleRO.from_dict({})
        assert ro.name == 'garbage'
