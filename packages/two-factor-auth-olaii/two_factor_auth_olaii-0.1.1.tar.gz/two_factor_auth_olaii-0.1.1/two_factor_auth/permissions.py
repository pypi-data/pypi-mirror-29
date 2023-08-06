from rest_framework import permissions

from two_factor_auth.views.utils import user_has_totp
from two_factor_auth.strings import TWO_FACTOR_AUTH_REQUIRED

from rest_framework import status
from rest_framework.exceptions import APIException


class TwoFactorAuthRequired(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = TWO_FACTOR_AUTH_REQUIRED

class HasTOTPEnabled(permissions.BasePermission):
    def has_permission(self, request, view):
        if user_has_totp(request.user):
            return True
        else:
            raise TwoFactorAuthRequired
