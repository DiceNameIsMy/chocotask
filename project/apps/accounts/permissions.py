from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.accounts.models import CustomUser


class IsEmployeeOrReadOnly(BasePermission):
    """
    The request is authenticated as a employee, or is a read-only request.
    """
    message = 'You must be an employee to perform this action.'

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.type == CustomUser.Type.EMPLOYEE
        )