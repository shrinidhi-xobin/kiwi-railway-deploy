import os

INSTALLED_APPS.append("social_django")
MIDDLEWARE.append("social_django.middleware.SocialAuthExceptionMiddleware")

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

# Optional: restrict logins to your company's Google Workspace domain
_allowed_domain = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAIN")
if _allowed_domain:
    SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = [_allowed_domain]

ROOT_URLCONF = "tcms_settings_dir.urls_with_social"