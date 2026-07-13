FROM kiwitcms/kiwi:latest

COPY nginx.conf /Kiwi/etc/nginx.conf
RUN pip install social-auth-app-django

COPY zzz_google_auth.py /tmp/zzz_google_auth.py
COPY urls_with_social.py /tmp/urls_with_social.py
COPY custom_login.html /tmp/custom_login.html

RUN TCMS_PKG_DIR=$(python -c "import tcms, os; print(os.path.dirname(tcms.__file__))") && \
    SITE_PACKAGES=$(dirname "$TCMS_PKG_DIR") && \
    mkdir -p "$SITE_PACKAGES/tcms_settings_dir" && \
    touch "$SITE_PACKAGES/tcms_settings_dir/__init__.py" && \
    cp /tmp/zzz_google_auth.py "$SITE_PACKAGES/tcms_settings_dir/zzz_google_auth.py" && \
    mkdir -p "$SITE_PACKAGES/kiwi_customizations" && \
    touch "$SITE_PACKAGES/kiwi_customizations/__init__.py" && \
    cp /tmp/urls_with_social.py "$SITE_PACKAGES/kiwi_customizations/urls_with_social.py" && \
    mkdir -p "$TCMS_PKG_DIR/templates/registration" && \
    cp /tmp/custom_login.html "$TCMS_PKG_DIR/templates/registration/custom_login.html"
