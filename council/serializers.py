from rest_framework import serializers
from .models import (
    Activity,
    Party,
    Promise,
)


class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = ('name',)


class RelatedActivitySerializer(serializers.RelatedField):
    def to_representation(self, value):
        try:
            image = value.image.url
        except ValueError:
            image = ''

        res = {
            'image': image, 'content': value.content,
            'created_at': value.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': value.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return res


class PromiseSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name', read_only=True)
    activity = RelatedActivitySerializer(queryset=Activity.objects.all(), many=True)

    class Meta:
        model = Promise
        fields = ('party_name', 'title', 'description', 'activity',)
        readonly_fields = ('party_name',)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('content', 'image',)
