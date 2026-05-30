from ._mixins import TimeStampModelMixin


class BaseModel(TimeStampModelMixin):
    class Meta:
        abstract = True
