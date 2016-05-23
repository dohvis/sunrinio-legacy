from rest_framework import viewsets
from rest_framework.response import Response

from dinner.models import Dinner
from dinner.serializers import DinnerSerializer


class DinnerViewSet(viewsets.ModelViewSet):
    """
    석식 거래 API

    <h2>status</h2>
    <ul>
    <li> 1: 판매중</li>
    <li> 2: 거래중</li>
    <li> 3: 판매 완료</li>
    </ul>
    """
    queryset = Dinner.objects.all()
    serializer_class = DinnerSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data.pop('price', None)  # protect to modify price
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
