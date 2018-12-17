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

    def test____init____raises_when_additional_fields(self):
        with pytest.raises(ValueError, match="iq"):
            Human(name='John', age=5, iq=None)

    def test____init____raises_when_missing_fields(self):
        with pytest.raises(ValueError, match="age"):
            Human(name='John')
