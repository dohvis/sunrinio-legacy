from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from teams.models import (
    Team,
    Want2Join,
)
from tags.models import Tag


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), many=True, slug_field='name', read_only=False)
    users = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='user-detail', many=True, read_only=False)

    def update(self, instance, validated_data):
        instance.users.clear()
        instance.users.add(*validated_data['users'])
        del validated_data['users']
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance

    def create(self, validated_data):
        instance = super(serializers.HyperlinkedModelSerializer, self).create(validated_data)
        instance.users.add(*validated_data['users'])  # Fucking ManyToManyRelation
        return instance

    class Meta:
        model = Team
        fields = ('url', 'name', 'tags', 'users', 'introduce', 'content')


class Want2JoinSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = serializers.HyperlinkedRelatedField(view_name='team-detail', read_only=True)

    class Meta:
        model = Want2Join
