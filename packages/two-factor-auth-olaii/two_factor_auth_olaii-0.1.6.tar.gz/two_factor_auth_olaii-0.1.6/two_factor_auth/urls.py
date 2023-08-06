from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from two_factor_auth.views.rest import TwoFactorAuthDetail, TwoFactorAuthEnableView, TwoFactorBackupCodeDetail, TestAPIView
from two_factor_auth.views.core import LoginView, BackupTokenView, SetupView, SetupCompleteView, QRGeneratorView
from two_factor_auth.views.profile import ProfileView, DisableView


urlpatterns = [
    # rest framework urls
    url(r"^$", TwoFactorAuthDetail.as_view(), name="two_factor_auth-detail"),
    url(r"^enable/$", TwoFactorAuthEnableView.as_view(), name="two_factor_auth-enable"),
    url(r"^backup_code_recovery/$", TwoFactorBackupCodeDetail.as_view(), name="backup_code-detail"),
    url(r"^test_api/$", TestAPIView.as_view(), name="test_api"),

    # urls for admin
    url(r"^login/$", LoginView.as_view(), name='login'),
    url(r"^profile/$", ProfileView.as_view(), name='profile'),
    url(r"^backup_token/$", BackupTokenView.as_view(), name='backup_token'),
    url(r"^disable/$", DisableView.as_view(), name='disable'),
    url(r"^setup/$", SetupView.as_view(), name='setup'),
    url(r"^setup/complete/$", SetupCompleteView.as_view(), name='setup_complete'),
    url(r"^qrcode/$", QRGeneratorView.as_view(), name='qr'),


]

urlpatterns = format_suffix_patterns(urlpatterns)
