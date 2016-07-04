from rest_framework import serializers
from accounts.models import User
from .models import (
    Board,
    Post,
)


class BoardSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField(
        view_name='post-detail',
        lookup_field='pk',
    )

    class Meta:
        model = Board
        fields = ('name', 'pk', 'posts')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')

    class Meta:
        model = Post
