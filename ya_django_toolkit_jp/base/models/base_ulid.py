from django_boost.models.mixins import TimeStampModelMixin

from .ulid import ULIDModel


class BaseULIDModel(TimeStampModelMixin, ULIDModel):
    class Meta:
        abstract = True
