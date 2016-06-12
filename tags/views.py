from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from accounts.models import Tag
from accounts.permissions import IsOwnerOrReadOnly
from tags.serializers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
