import re

from django import template

register = template.Library()

_LOCALE_PREFIX_RE = re.compile(r"^/[a-z]{2}(-[a-z]{2})?/")


@register.filter
def startswith(text, prefix):
    if not isinstance(text, str):
        return False
    text = _LOCALE_PREFIX_RE.sub("/", text)
    return text.startswith(prefix)
