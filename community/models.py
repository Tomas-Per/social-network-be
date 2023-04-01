from django.conf import settings
from django.db import models

from socialnetwork.utils.mixins import DefaultUUIDMixin, DefaultValuesMixin


class Community(DefaultUUIDMixin, DefaultValuesMixin):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="subscribed_communities", blank=True
    )

    class Meta:
        verbose_name_plural = "Communities"

    def __str__(self) -> str:
        return self.name
