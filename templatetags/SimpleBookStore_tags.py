from django import template
from django.utils.html import escape
from django.contrib.auth.models import User
from six.moves.urllib.parse import urlencode, urlparse, parse_qs
from django.core.urlresolvers import reverse
import hashlib

register = template.Library()


@register.simple_tag
def following_status(id, list):
    return 1 if id in list else 0
