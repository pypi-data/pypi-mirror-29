Olaii Two-Factor Authentication for Django.
===========================================

Based on [django-two-factor-auth](https://github.com/Bouke/django-two-factor-auth) (for admin) and [Deux](https://github.com/robinhood/deux) (for Oauth2).

### Requirements
```
Django >= 1.11
Python >= 2.7
django_otp >= 0.4.2
qrcode >= 5.3
django_formtools >= 2.1
```

## Installation

You can install it from PyPI using `pip`:

```
$ pip install two_factor_auth_olaii
```

### Setup

Add `two_factor_auth` and `django_otp` to your INSTALLED\_APPS setting like this::

```
INSTALLED_APPS = (
    ...
    'two_factor_auth',
    'django_otp',
)
```

Add the `django-otp` middleware to your `MIDDLEWARE`. Make sure it comes after `AuthenticationMiddleware`:

```
MIDDLEWARE = (
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    ...
)
```

Add following in your `settings.py`:
```
LOGIN_URL = 'two_factor_auth:login'
LOGIN_REDIRECT_URL = 'two_factor_auth:profile'
TOTP_DIGITS = 6 # Google Authenticator allowes only 6 digits
# specifiy your app name
TOTP_ISSUER = "App Name"
```

Include `two_factor_auth` URLconf in your project urls.py like this:
```
urlpatterns = [
   url(r'^two_factor/', include('two_factor_auth.urls', namespace="two_factor_auth")),
    ...
]
```

### Admin Site

By default the admin login is patched to use the login views provided by this application. Patching the admin is required as users would otherwise be able to circumvent TOTP verification. In order to only allow verified users (enforce TOTP) to access the admin pages, you have to use a custom admin site. If you want to enforce two factor authentication in the admin and use the default admin site, you can monkey patch the default `AdminSite` with this. In your `urls.py`:

```
from django.contrib import admin
from two_factor_auth.admin import AdminSiteTOTPRequired

admin.site.__class__ = AdminSiteTOTPRequired

urlpatterns = [
    url(r'^admin/', admin.site.urls),
...
]
```

### Using Oauth2

Add the following to `urls.py`:

```
urlpatterns = [
    url(r'^two_factor/o/', include("two_factor_auth.oauth2.urls", namespace="two_factor_auth-oauth2:login")),
...
]
```
For oauth2, place the request to **POST** `/two_factor/o/token` with a `password` grant type.

### Other packages with custom login views

Be aware that certain packages include their custom login views, for example django.contrib.admindocs. When using said packages, TOTP verification can be circumvented. Thus however the normal admin login view is patched, TOTP might not always be enforced on the admin views. You can enforce two-factor authentication by overriding the `login` url.

For instance when using `Django Rest Framework`, do the following in `urls.py`:
```
from django.contrib import admin
from two_factor_auth.admin import AdminSiteTOTPRequired

admin.site.__class__ = AdminSiteTOTPRequired

urlpatterns = [
    url(r'^api-auth/login/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
...
]
```

Run `python manage.py migrate` to create the mangopayments models.

### Limiting access to certain API views

API views can be limited to two-factor-enabled users. If you wish to secure certain parts of the website add `HasTOTPEnabled` to `permission_classes`.

```
from two_factor_auth.permissions import HasTOTPEnabled

class SomeAPIView(APIView):
    permission_classes = (HasTOTPEnabled,)
    ...
```

