from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from django.http import JsonResponse
from teams.models import (
    Team,
    Want2Join,
)


class Want2JoinView(CreateAPIView):
    def post(self, request, team_id):
        user = request.user
        team = get_object_or_404(Team, id=team_id)
        Want2Join.objects.create(user=user, team=team)
        return JsonResponse({'status': 'success'})
