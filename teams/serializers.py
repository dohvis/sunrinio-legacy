from rest_framework import serializers
from accounts.models import User
from teams.models import Team


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', many=True)

    class Meta:
        model = Team
        fields = ('url', 'name', 'tags', 'users', 'introduce', 'content')
