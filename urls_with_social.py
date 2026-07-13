from django.urls import include, re_path
from tcms.urls import urlpatterns as _tcms_urlpatterns

urlpatterns = [
    re_path(r"^", include("social_django.urls", namespace="social")),
] + _tcms_urlpatterns
