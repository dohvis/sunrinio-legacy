from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework import permissions
from teams.permissions import IsMemberOrReadonly
from teams.models import (
    Team,
    Want2Join,
)

from teams.serializers import (
    TeamSerializer,
    Want2JoinSerializer,
)
from accounts.models import User

class TeamViewSet(ModelViewSet):
    """
    팀 정보 조회 API
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    permission_classes = (permissions.IsAuthenticated,
                          IsMemberOrReadonly)


class Want2JoinViewSet(ModelViewSet):
    """
    팀 가입 신청 API
    """
    queryset = Want2Join.objects.all()
    serializer_class = Want2JoinSerializer

    permission_classes = (permissions.IsAuthenticated,
                          IsMemberOrReadonly)

    def create(self, request, *args, **kwargs):
        pk = kwargs['pk']
        team = get_object_or_404(Team, pk=pk)

        message = request.POST['message']
        Want2Join.objects.create(team=team, user=request.user, message=message)
        return JsonResponse({'message': '가입신청 되었습니다. 결과를 기다려 주세요.'}, status=201)

    def get_queryset(self):
        from re import search
        pk = search(r"\d+", self.request._request.path).group(0)
        try:
            qs = Want2Join.objects.filter(team__pk=pk)
        except Team.DoesNotExist:
            return None
        return qs
