from uuid import uuid4

from django.conf import settings
from django.db import models


class DefaultUUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class DefaultValuesMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(class)s_created_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="%(class)s_updated_by", on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
