from rest_framework import serializers

from accounts.models import User
from tags.models import Tag
from teams.models import Team


class TagSerializer(serializers.HyperlinkedModelSerializer):
    teams = serializers.HyperlinkedRelatedField(queryset=Team.objects.all(), view_name='team-detail', many=True)
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', many=True)

    class Meta:
        model = Tag
        fields = ('name', 'teams', 'users')
