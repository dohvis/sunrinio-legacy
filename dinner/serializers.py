from rest_framework import serializers

from dinner.models import Dinner


class DinnerSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.IntegerField(default=1000)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Dinner
        fields = ('seller', 'date', 'price', 'status')
