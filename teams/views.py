from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.viewsets import ReadOnlyModelViewSet

from teams.models import (
    Team,
    Want2Join,
)

from teams.serializers import TeamSerializer


class TeamViewSet(ReadOnlyModelViewSet):
    """
    팀 정보 조회 API
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class Want2JoinView(View):
    """
    팀 가입 요청 API
    """
    def post(self, request, team_id):
        """
        :param request: request 객체
        :param team_id: 들어가기를 희망하는 팀의 고유 id
        :return: {'status':'success'}
        """
        user = request.user
        team = get_object_or_404(Team, id=team_id)
        Want2Join.objects.create(user=user, team=team)
        return JsonResponse({'status': 'success'})
