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
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class Want2JoinView(View):
    def post(self, request, team_id):
        user = request.user
        team = get_object_or_404(Team, id=team_id)
        Want2Join.objects.create(user=user, team=team)
        return JsonResponse({'status': 'success'})
