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


class ActivitySerializer(serializers.RelatedField):
    def to_representation(self, value):
        try:
            image = value.image.url
        except ValueError:
            image = ''

        return {'image': image, 'content': value.content}


class PromiseSerializer(serializers.ModelSerializer):
    party_name = serializers.CharField(source='party.name')
    details = ActivitySerializer(queryset=Activity.objects.all(), many=True)

    class Meta:
        model = Promise
        fields = ('party_name', 'title', 'description', 'details',)


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
