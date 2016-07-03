from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Board
from .serializers import BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        self.request.GET.pop('board')