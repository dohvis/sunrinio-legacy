from rest_framework import viewsets
from rest_framework.response import Response

from council.models import (
    Activity,
    Party,
    Promise,
)
from council.serializers import (
    ActivitySerializer,
    PartySerializer,
    PromiseSerializer,
)


class DetailViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()

    def get_queryset(self):
        from re import search
        pk = search(r"\d+", self.request._request.path).group(0)
        return Activity.objects.filter(promise__pk=pk)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data.pop('price', None)  # protect to modify price
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data.pop('price', None)  # protect to modify price
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PromiseViewSet(viewsets.ModelViewSet):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
