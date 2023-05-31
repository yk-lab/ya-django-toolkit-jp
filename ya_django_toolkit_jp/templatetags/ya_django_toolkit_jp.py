from __future__ import annotations

from logging import getLogger

from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import escape_uri_path

logger = getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def is_active_view(context, *view_names):
    request = context.get('request')

    _view_names = []
    for v in view_names:
        if isinstance(v, str):
            _view_names.append(v)
        elif isinstance(v, (list, tuple)):
            _view_names.extend(v)
        else:
            raise ValueError('Invalid view name.')

    view_name = getattr(request.resolver_match, 'view_name')
    return view_name and view_name in _view_names or False


@register.simple_tag(takes_context=True)
def is_active_link(context, view_name, *args, **kwargs):
    request = context.get('request')

    try:
        path = reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return False

    request_path = escape_uri_path(request.path)

    return path == request_path
