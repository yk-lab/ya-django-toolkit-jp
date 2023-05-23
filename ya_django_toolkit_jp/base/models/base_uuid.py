from django_boost.models.mixins import TimeStampModelMixin, UUIDModelMixin


class BaseUUIDModel(TimeStampModelMixin, UUIDModelMixin):
    class Meta:
        abstract = True
