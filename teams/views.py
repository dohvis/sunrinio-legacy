from django.shortcuts import get_object_or_404, render
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


def team_list(request):
    return render(request, 'teams/list.html')


def team_add(request):
    return render(request, 'teams/teammaker.html')


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    joins = Want2Join.objects.filter(team=team)
    isowner = request.user in team.members.all()
    return render(request, 'teams/detail.html', context={'team': team, 'joins': joins, 'isowner': isowner})


def team_join(request, pk):
    team = get_object_or_404(Team, pk=pk)
    joins = Want2Join.objects.filter(team=team)
    if request.user in team.members.all():
        return render(request, 'alert.html', context={'message': '이미 팀의 멤버입니다!', 'location': '/teams/'+pk})

    already_joined = False
    for join in joins:
        if request.user == join.user:
            already_joined = True

    if already_joined:
        return render(request, 'alert.html', context={'message': '이미 가입 신청하였습니다!', 'location': '/teams/'+pk})

    Want2Join(team=team, user=request.user).save()
    return render(request, 'alert.html', context={'message': '가입 신청 되었습니다!', 'location': '/teams/'+pk})


def team_member_delete(request, pk, user_pk):
    """
    팀 멤버 삭제
    :param pk: team pk
    :param user_pk: user pk
    """
    team = get_object_or_404(Team, pk=pk)
    if request.user not in team.members.all():
        return render(request, 'alert.html', context={'message': '권한이 없습니다!', 'location': '/teams/'+pk})
    delete_target = User.objects.get(pk=user_pk)
    team.members.remove(delete_target)
    if team.members.count() == 0:
        """
        마지막 남은 팀원이 자신을 삭제할 때 팀도 삭제합니다.
        """
        team.delete()
    return render(request, 'alert.html', context={'message': '성공적으로 삭제되었습니다!', 'location': '/teams/'+pk})


def team_join_request_accept(request, pk, user_pk):
    team = get_object_or_404(Team, pk=pk)
    target = get_object_or_404(User, pk=user_pk)
    join = get_object_or_404(Want2Join, team=team, user=target)
    if request.user not in team.members.all():
        return render(request, 'alert.html', context={'message': '권한이 없습니다!', 'location': '/teams/'+pk})
    join.delete()
    team.members.add(target)
    return render(request, 'alert.html', context={'message': '성공적으로 추가하였습니다!', 'location': '/teams/'+pk})


def team_join_request_reject(request, pk, user_pk):
    team = get_object_or_404(Team, pk=pk)
    target = get_object_or_404(User, pk=user_pk)
    join = get_object_or_404(Want2Join, team=team, user=target)
    if request.user not in team.members.all():
        return render(request, 'alert.html', context={'message': '권한이 없습니다!', 'location': '/teams/'+pk})
    join.delete()
    return render(request, 'alert.html', context={'message': '요청이 거절되었습니다.', 'location': '/teams/'+pk})
