from rest_framework import serializers
from .models import (
    Place,
    Review,
)


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    reviews = serializers.HyperlinkedIdentityField(view_name='review-detail', many=True)

    class Meta:
        model = Place
        fields = ('name', 'address', 'description', 'location', 'reviews')


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ('place', 'user', 'rate', 'comment')
