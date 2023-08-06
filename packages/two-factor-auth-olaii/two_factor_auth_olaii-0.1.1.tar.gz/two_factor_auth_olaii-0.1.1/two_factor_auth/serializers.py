from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from two_factor_auth.models import Totp
from two_factor_auth.strings import DISABLED_ERROR


class TwoFactorAuthSerializer(serializers.ModelSerializer):
    """
    class::TwoFactorAuthSerializer()

    Basic TwoFactorAuthSerializer that encodes Totp objects into a standard
    response.

    The standard response returns whether Totp is enabled.
    """

    class Meta:
        model = Totp
        fields = ('id', 'enabled',)


class TwoFactorAuthEnableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Totp
        fields = ('id', 'config_url', 'backup_code')

    def update(self, totp_instance, validated_data):
        if not totp_instance.enabled:
            totp_instance.enabled = True
            totp_instance.refresh_backup_code()
            totp_instance.save()

        return totp_instance


class TwoFactorAuthBackupCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Totp
        fields = ('id', 'backup_code')

    def update(self, totp_instance, validated_data):
        if totp_instance.enabled:
            totp_instance.refresh_backup_code()
        else:
            raise serializers.ValidationError({"error": DISABLED_ERROR})

        return totp_instance
