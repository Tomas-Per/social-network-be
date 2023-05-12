from rest_framework import status, viewsets

from community.models import Community
from community.serializers import CommunitySerializer
from community.tasks import delete_community_from_elastic, sync_community_to_elastic
from socialnetwork.utils.filters import CommunityFilter
from socialnetwork.utils.permissions import OwnerAuthenticatedOrReadOnlyPermission


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filterset_class = CommunityFilter
    permission_classes = [OwnerAuthenticatedOrReadOnlyPermission]

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            sync_community_to_elastic.delay(response.data["id"])
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            sync_community_to_elastic.delay(response.data["id"])
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            delete_community_from_elastic.delay(kwargs["pk"])
        return response
