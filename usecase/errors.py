from usecase.privilege import Privilege


class UseCaseError(Exception):
    """Base class for Use cases exceptions"""


class ObjectDoesNotExist(UseCaseError):
    """A requested object does not exist (equivalent of HTTP 404)"""


class UserNotAuthenticatedError(UseCaseError):
    """Action requires user to be authenticated (equivalent of HTTP 401)"""


class UserNotPermitted(UseCaseError):
    """User is not allowed to access a certain resource (equivalent of HTTP 403)"""


class MissingPrivilegeError(UseCaseError):
    """Action requires a specific privilege (equivalent of HTTP 401)"""
    def __init__(self, privilege):
        msg = privilege.name if isinstance(privilege, Privilege) else privilege
        super(MissingPrivilegeError, self).__init__(msg)


class RestrictedToRootError(UserNotPermitted):
    """Access to a certain resource requires root privilege (equivalent of HTTP 403)"""


class ActionCantBePerformed(UseCaseError):
    """Action cant be performed"""
    pass
