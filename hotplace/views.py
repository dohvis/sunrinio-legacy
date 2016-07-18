from django.shortcuts import (
    get_object_or_404,
    render,
    redirect,
    HttpResponse,
)
from rest_framework import viewsets
from rest_framework.response import Response
from accounts.models import User
from .models import (
    Place,
    Review,
)
from .forms import PlaceReviewForm
from .serializers import PlaceSerializer, ReviewSerializer


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer
    read_only = True
    queryset = Place.objects.all()

    def list(self, request, *args, **kwargs):
        ne = [float(x) for x in self.request.query_params.get('ne', '43.0,132.0').split(",")]
        sw = [float(x) for x in self.request.query_params.get('sw', '33.0,124.0').split(",")]
        # 우리나라 위도 경도 범위 참고해서 우리나라 전범위
        # 위도(y),경도(x) 범위: (124.0, 132.0) (33.0, 43.0)
        x_range = (sw[1], ne[1],)
        y_range = (sw[0], ne[0],)
        print(x_range, y_range)
        queryset = Place.objects.filter(x__range=x_range, y__range=y_range)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)


def mapview(request):
    return render(request, 'hotplace/map.html')


def place_detail(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    context = {'place': place}
    return render(request, 'hotplace/detail.html', context)


def add_review(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if request.method == 'GET':
        form = PlaceReviewForm()
    elif request.method == 'POST':
        form = PlaceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = Place.objects.get(pk=place_pk)
            review.user = request.user
            review.save()
            return redirect('/hotplace/{}/'.format(place_pk))
        else:
            print(form.errors)
            return HttpResponse(status=400)

    else:
        form = PlaceReviewForm()

    context = {'place': place, 'form': form}
    return render(request, 'hotplace/review.html', context)
