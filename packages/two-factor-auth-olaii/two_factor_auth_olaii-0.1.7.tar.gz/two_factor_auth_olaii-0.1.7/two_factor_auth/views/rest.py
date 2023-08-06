from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from two_factor_auth.models import Totp
from two_factor_auth.serializers import TwoFactorAuthSerializer, TwoFactorAuthEnableSerializer, TwoFactorAuthBackupCodeSerializer
from two_factor_auth.permissions import HasTOTPEnabled


class TwoFactorAuthMixin(object):
    """
    Mixin that defines queries for Totp objects.
    """

    def get_object(self):
        """Gets the current user's Totp instance"""
        instance, created = Totp.objects.get_or_create(user=self.request.user)
        return instance


class TwoFactorAuthDetail(TwoFactorAuthMixin, generics.RetrieveDestroyAPIView):
    """
    class::TwoFactorAuthDetail()

    View for requesting data about TwoFactorAuth and deleting Totp.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TwoFactorAuthSerializer

    def perform_destroy(self, instance):
        """
        The delete method should disable Totp for this user.

        :raises rest_framework.exceptions.ValidationError: If MFA is not
            enabled.
        """
        instance.enabled = False
        instance.save()


class TwoFactorAuthEnableView(TwoFactorAuthMixin, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TwoFactorAuthEnableSerializer


class TwoFactorBackupCodeDetail(TwoFactorAuthMixin, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TwoFactorAuthBackupCodeSerializer


class TestAPIView(TwoFactorAuthMixin, generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, HasTOTPEnabled, )
    serializer_class = TwoFactorAuthSerializer