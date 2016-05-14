from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import render

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


class FacebookOAuth2AdapterCustom(FacebookOAuth2Adapter):
    def __init__(self):
        pass


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2AdapterCustom


def signin(requests):
    return render(requests, "accounts/signin.html")
