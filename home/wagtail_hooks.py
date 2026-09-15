from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css():
    """Load the custom brand theme across the whole Wagtail admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/wagtail-admin-theme.css")
    )
