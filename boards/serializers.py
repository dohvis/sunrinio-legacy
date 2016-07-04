from rest_framework import serializers
from accounts.models import User
from tags.models import Tag
from .models import (
    Board,
    Post,
)


class BoardSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='post-detail',
        read_only=True,
    )

    class Meta:
        model = Board


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    board = serializers.SlugRelatedField(queryset=Board.objects.all(), slug_field='name')
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), slug_field='name', many=True)

    class Meta:
        model = Post
