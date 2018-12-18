from unittest.mock import Mock

import formencode as fe
import pytest

from usecase.errors import MissingPrivilegeError, UserNotAuthenticatedError
from usecase.privilege import Privilege
from usecase.request_object import UseCaseRequestObject
from usecase.use_case import UseCase


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

    # def __init__(self, logged_user=None):
    #     self.logged_user = logged_user
    #
    # def execute(self, req_obj=None, *args, **kwargs):
    #     if self.privilege:
    #         self._verify_logged_user()
    #         self._verify_privilege()
    #
    #     assert isinstance(req_obj, self.request_object), f'{type(req_obj)} request object is not of type {self.request_object}'
    #     return self._execute(req_obj, *args, **kwargs)
    #
    # def _verify_privilege(self):
    #     privilege = self.privilege
    #     logged_user = self.logged_user
    #
    #     if not logged_user.has_privilege(privilege):
    #         raise MissingPrivilegeError(f"{logged_user} is missing privilege {privilege.name}")
    #
    # def _verify_logged_user(self):
    #     if not self.logged_user:
    #         raise UserNotAuthenticatedError('No user is logged for {}'.format(self.__class__.__name__))
    #
    # @abc.abstractmethod
    # def _execute(self, req_obj):
    #     pass


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
