from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css():
    """Load the custom brand theme across the whole Wagtail admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/wagtail-admin-theme.css")
    )


@hooks.register("insert_global_admin_js")
def global_admin_js():
    """Progressive-enhancement JS for finer-grained status badge colors."""
    return format_html(
        '<script src="{}"></script>', static("js/wagtail-admin-theme.js")
    )
