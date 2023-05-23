from __future__ import annotations

from django.urls import ResolverMatch


def get_viewname_with_appname(viewname: str, appname: str | None = None, *,
                              default_appname: str | None = None,
                              resolver_match: ResolverMatch | None = None):
    if appname is None:
        if resolver_match:
            appname = resolver_match.app_name
        else:
            appname = default_appname
    return f'{appname}:{viewname}' if appname else f'{viewname}'
