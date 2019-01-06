import formencode as fe
import pytest

from usecase.errors import MissingPrivilegeError, UserNotAuthenticatedError
from usecase.privilege import Privilege
from usecase.request_object import UseCaseRequestObject
from usecase.use_case import UseCase, use_case_config

sample_privilege1 = Privilege(
        name='SamplePrivilege',
        description='whatever',
        categories=['A', 'B'])


class SampleRO(UseCaseRequestObject):
    name = fe.validators.String(not_empty=True)


class SampleUseCase(UseCase):
    privilege = sample_privilege1
    request_object = SampleRO

    def _execute(self, req_obj):
        return True


@pytest.fixture()
def logged_user():
    class User(object):
        def __init__(self, privileges):
            self.privileges = privileges

        def has_privilege(self, privilege):
            privileges_names = {p.name for p in self.privileges}
            return privilege.name in privileges_names

    return User(privileges=[sample_privilege1])


class TestUseCase:
    def test____init____(self, logged_user):
        uc = SampleUseCase(logged_user=logged_user)
        assert uc.logged_user is logged_user

    def test__execute__returns(self, logged_user):
        ro = SampleRO(name='John')
        uc = SampleUseCase(logged_user=logged_user)
        assert uc.execute(ro) is True

    def test__execute__raises_UserNotAuthenticatedError(self):
        with pytest.raises(UserNotAuthenticatedError):
            uc = SampleUseCase(logged_user=None)
            uc.execute()

    def test__execute__raises_MissingPrivilegeError(self, logged_user):
        logged_user.privileges = []

        ro = SampleRO(name='John')
        with pytest.raises(MissingPrivilegeError):
            uc = SampleUseCase(logged_user=logged_user)
            uc.execute(ro)

    def test__execute__dont_accept_wrong_request_object(self, logged_user):
        class WrongRO(UseCaseRequestObject):
            pass

        wrong_ro = WrongRO()
        uc = SampleUseCase(logged_user=logged_user)
        with pytest.raises(ValueError, match="request object provided to use case is not of type"):
            uc.execute(wrong_ro)

    def test__execute_using_simple_dict_as_request_object(self, logged_user):
        class SampleUseCase(UseCase):
            request_object = dict

            def _execute(self, req_obj):
                return True

        uc = SampleUseCase()
        assert uc.execute(req_obj={'test': 1}) is True


class TestUseCaseUtils:
    def test_use_case_config(self, logged_user):

        @use_case_config(sample_privilege1, SampleRO)
        class DecoratedUseCase(UseCase):
            def _execute(self, req_obj):
                return True

        assert DecoratedUseCase.privilege is sample_privilege1
        assert DecoratedUseCase.request_object is SampleRO

        ro = SampleRO(name='John')
        uc = DecoratedUseCase(logged_user=logged_user)
        assert uc.execute(ro) is True
