from django.contrib import admin

from community.models import Community
from socialnetwork.utils.mixins import BaseAdminMixin


@admin.register(Community)
class CommunityAdmin(BaseAdminMixin):
    pass
