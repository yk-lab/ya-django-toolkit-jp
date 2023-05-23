from django_boost.models.mixins import TimeStampModelMixin


class BaseModel(TimeStampModelMixin):
    class Meta:
        abstract = True
