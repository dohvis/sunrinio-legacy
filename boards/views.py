from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Board,
    Post,
)
from .serializers import (
    BoardSerializer,
    PostSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        pk = self.request.GET.get('pk', False)
        if pk:
            queryset = Board.objects.filter(pk=pk)
        else:
            queryset = Board.objects.all()
        return queryset


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
