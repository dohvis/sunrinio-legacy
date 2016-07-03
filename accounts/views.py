from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import (
    HttpResponse,
    render,
)

from accounts.models import User
from accounts.permissions import IsOwnerOrReadOnly
from accounts.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FacebookOAuth2AdapterCustom(FacebookOAuth2Adapter):
    def __init__(self):
        pass


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2AdapterCustom


def login(request):
    return render(request, "accounts/login.html")


def update_profile_image(request):
    # TODO: POST말고 다른 메소드로는 파일업로드가 안되서 우선 임시로 프사변경만 API따로 만들어둠
    if request.method != 'POST':
        return HttpResponse(status=400)
    img = request.FILES['profile_image']
    user = request.user
    user.profile_image = img
    user.save()
    return HttpResponse(status=200)
