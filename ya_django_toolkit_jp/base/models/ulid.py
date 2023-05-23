from django.db import models

from ...fields import ULIDField


class ULIDModel(models.Model):
    id = ULIDField(
        primary_key=True,
        editable=False,
    )

    class Meta:
        abstract = True
