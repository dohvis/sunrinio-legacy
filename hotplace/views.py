from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import (
    Place,
    Review,
)
from .serializers import PlaceSerializer, ReviewSerializer


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer
    read_only = True
    queryset = Place.objects.all()

    def list(self, request, *args, **kwargs):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """

        user = self.request.user
        x = self.request.query_params.get('x', '1.0')
        y = self.request.query_params.get('y', '1.0')
        queryset = Place.objects.filter()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)
