from rest_framework import serializers
from rest_framework import viewsets
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ScheduleSerializer
    read_only = True
    queryset = Schedule.objects.all()
