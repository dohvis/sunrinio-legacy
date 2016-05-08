from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.models import Tag, User
from accounts.permissions import IsOwnerOrReadOnly
from accounts.serializers import UserSerializer, TagSerializer


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
