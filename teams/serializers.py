from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from teams.models import (
    Team,
    Want2Join,
)


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', many=True)

    class Meta:
        model = Team
        fields = ('url', 'name', 'tags', 'users', 'introduce', 'content')


class Want2JoinSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Want2Join
