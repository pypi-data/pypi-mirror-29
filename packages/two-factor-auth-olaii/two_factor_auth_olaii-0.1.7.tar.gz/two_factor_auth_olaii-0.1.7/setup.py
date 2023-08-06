from setuptools import setup, find_packages

setup(
  name = 'two_factor_auth_olaii',
  packages=['two_factor_auth'],
  package_data = {'two_factor_auth': ['migrations/*', 'templates/*', 'oauth2/*', 'views/*']},
  include_package_data=True,
  version = '0.1.7',
  description = 'Two-factor authentication for Django based on django-two-factor-auth and deux.',
  author = 'Polona Remic',
  author_email = 'polona@olaii.com',
  url = 'https://gitlab.xlab.si/olaii/Olaii_2FA',
  download_url = 'https://gitlab.xlab.si/olaii/Olaii_2FA',
  install_requires=[
        'Django>=1.11',
        'django_otp>=0.4.2,<0.99',
        'qrcode>=5.3',
        'django-formtools',
  ],
  keywords = ['django', 'two-factor authentication'], # arbitrary keywords
  classifiers = [],
)

