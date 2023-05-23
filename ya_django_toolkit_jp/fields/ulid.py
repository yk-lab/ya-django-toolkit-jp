from django.db import models

try:
    from ulid import providers
    from ulid.api import api
except ImportError:
    providers = None
    api = None


def default():
    if not providers or not api:
        raise ImportError('ULIDField requires ulid package.')

    ulid_api = api.Api(providers.DEFAULT)
    return ulid_api.new().uuid


class ULIDField(models.UUIDField):
    def __init__(self, primary_key=True, editable=False, *args, **kwargs):
        if not providers or not api:
            raise ImportError('ULIDField requires ulid package.')

        kwargs.setdefault('primary_key', primary_key)
        kwargs.setdefault('editable', editable)
        kwargs.setdefault('default', default)
        super().__init__(*args, **kwargs)
