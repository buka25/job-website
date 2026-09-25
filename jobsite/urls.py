from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("i18n/", include("django.conf.urls.i18n")),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static files from the development server -- WhiteNoise
    # (see MIDDLEWARE) handles this in production instead.
    urlpatterns += staticfiles_urlpatterns()

# Media (user-uploaded images/documents) has no dedicated object storage
# (S3, etc.) configured, so it's served directly by the app in every
# environment, not just DEBUG -- otherwise production would 404 on
# every uploaded file. Fine at this site's scale; revisit if traffic
# or storage needs grow enough to warrant a CDN/S3.
from django.conf.urls.static import static  # noqa: E402

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    path("search/suggest/", search_views.search_suggest, name="search_suggest"),
    path("", include(wagtail_urls)),
)