import os
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
from tcms.settings.common import INSTALLED_APPS as _BASE_APPS, MIDDLEWARE as _BASE_MIDDLEWARE
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
INSTALLED_APPS = _BASE_APPS + ["social_django"]
MIDDLEWARE = _BASE_MIDDLEWARE + ["social_django.middleware.SocialAuthExceptionMiddleware"]
DEBUG = True

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

_allowed_domain = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAIN")
if _allowed_domain:
    SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = [_allowed_domain]

ROOT_URLCONF = "kiwi_customizations.urls_with_social"
