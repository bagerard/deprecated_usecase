import abc

from usecase.errors import MissingPrivilegeError, UserNotAuthenticatedError
from usecase.privilege import Privilege
from usecase.request_object import RequestObjectMeta

NoPrivilege = None  # Sentinel that can be used to identify use case that don't need privileges

NoneType = type(None)


def use_case_config(privilege=None, request_object=NoneType):
    """Class decorator that allows to attach a privilege and a request_object class
    to a certain use case class

    Usage:

    @use_case_config(Privileges.ListStudies, ListStudiesRO)
    class ListStudiesUC(UseCase):
        pass


    :param privilege: The privilege required by the use case
    :type privilege: privilege
    :param request_object: a RequestObject class
    :type request_object: UseCaseRequestObject class
    :return: the decorated class
    :rtype: cls
    """
    def class_rebuilder(cls):
        assert isinstance(privilege, (Privilege, NoneType))
        assert isinstance(request_object, (RequestObjectMeta)) or request_object is NoneType

        cls.privilege = privilege
        cls.request_object = request_object
        return cls
    return class_rebuilder


class UseCase(object, metaclass=abc.ABCMeta):
    privilege = None                # Will require a logged_user by definition
    request_object = NoneType     # class of the RequestObject attached to the use case

    def __init__(self, logged_user=None):
        self.logged_user = logged_user

    def execute(self, req_obj=None, *args, **kwargs):
        if self.privilege:
            self._verify_logged_user()
            self._verify_privilege()

        if not isinstance(req_obj, self.request_object):
            req_obj_cls = req_obj.__class__.__name__
            raise ValueError(f'{req_obj_cls} request object provided to use case is not of type {self.request_object}')
        return self._execute(req_obj, *args, **kwargs)

    def _verify_privilege(self):
        privilege = self.privilege
        logged_user = self.logged_user

        if not logged_user.has_privilege(privilege):
            raise MissingPrivilegeError(f'{logged_user} is missing privilege {privilege.name}')

    def _verify_logged_user(self):
        if not self.logged_user:
            raise UserNotAuthenticatedError(f'No user is logged for {self.__class__.__name__}')

    @abc.abstractmethod
    def _execute(self, req_obj):
        pass
