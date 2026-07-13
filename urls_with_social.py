from django.urls import include, re_path
from tcms.urls import urlpatterns as _tcms_urlpatterns

urlpatterns = _tcms_urlpatterns + [
    re_path(r"^", include("social_django.urls", namespace="social")),
]