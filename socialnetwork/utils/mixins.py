from collections import OrderedDict
from uuid import uuid4

from django.conf import settings
from django.contrib import admin
from django.db import models
from rest_framework import serializers


class DefaultUUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class DefaultValuesMixin(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created_by",
        on_delete=models.CASCADE,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updated_by",
        on_delete=models.CASCADE,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseAdminMixin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at", "created_by", "updated_by"]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class BaseSerializerMixin(serializers.ModelSerializer):
    def validate(self, validated_data: OrderedDict) -> OrderedDict:
        user = self.context["request"].user
        validated_data.update({"created_by": user}) if not self.instance else None
        validated_data.update({"updated_by": user})
        return super().validate(validated_data)
