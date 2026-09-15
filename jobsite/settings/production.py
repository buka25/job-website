import os

from .base import *

DEBUG = False

# SECRET_KEY has no fallback on purpose: the app must refuse to start
# rather than silently run production traffic on a leaked/example key.
SECRET_KEY = os.environ["SECRET_KEY"]

# No fallback here either: an empty list is a *safe* failure (Django
# rejects every request with 400 Bad Request) rather than a wildcard
# that would silently accept any Host header.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# Needed whenever the site is served over HTTPS and admin/API POSTs come
# from that same origin (Django checks this independently of ALLOWED_HOSTS).
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# Base URL used when Wagtail builds full URLs outside of a request
# context (e.g. notification/password-reset emails). Don't include
# '/admin' or a trailing slash.
WAGTAILADMIN_BASE_URL = os.environ.get(
    "WAGTAILADMIN_BASE_URL", "http://example.com"
)

# ---- HTTPS / cookie security ----
# Assumes the app sits behind a reverse proxy (nginx, or a PaaS's own
# load balancer) that terminates TLS and forwards the original scheme
# in this header -- true for the common VPS-with-nginx and PaaS setups
# alike. Set SECURE_SSL_REDIRECT=false only if TLS isn't available yet
# (e.g. testing a deploy before DNS/certs are ready).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "true").lower() == "true"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 60 * 60 * 24 * 30))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ---- Email ----
# Contact-form notifications and password-reset emails need a real SMTP
# provider in production -- the console backend from dev.py only prints
# to stdout. Any standard SMTP provider works (e.g. an org mailbox,
# SendGrid, Mailgun, Postmark).
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "true").lower() == "true"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade). WhiteNoise's variant additionally
# gzip/brotli-compresses files and serves them straight from gunicorn,
# so a separate nginx static-file config isn't required.
# See https://docs.djangoproject.com/en/6.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

# ---- Logging ----
# Sends Django's own error/warning output to stdout/stderr, which every
# common deploy target (systemd journal, Railway, Render, Heroku) already
# captures -- without this, a 500 error in production leaves no trace
# anywhere.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
