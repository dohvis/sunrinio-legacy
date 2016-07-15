from rest_framework import serializers
from .models import (
    Place,
    Review,
)


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    reviews = serializers.SlugRelatedField(slug_field='comment', queryset=Review.objects.all(), many=True)

    class Meta:
        model = Place
        exclude_fields = ('location',)


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ('place', 'user', 'rate', 'comment')
