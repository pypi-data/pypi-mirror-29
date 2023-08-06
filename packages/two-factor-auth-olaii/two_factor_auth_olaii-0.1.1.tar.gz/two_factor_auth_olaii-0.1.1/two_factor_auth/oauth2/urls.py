from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from two_factor_auth.oauth2 import views

urlpatterns = [
    url(r'^token/$', views.TwoFactorAuthTokenView.as_view(), name="token"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
