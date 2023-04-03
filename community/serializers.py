from community.models import Community
from socialnetwork.utils.mixins import BaseSerializerMixin


class CommunitySerializer(BaseSerializerMixin):
    class Meta:
        model = Community
        fields = "__all__"
