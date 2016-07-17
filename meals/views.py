from django.shortcuts import render, HttpResponse
from .models import Meal


def meal_view(request):
    if request.method == 'POST':
        # Meal.objects.create()
        pass
    elif request.method != 'GET':
        return HttpResponse(status=401)
    else:
        pass
    return render(request, 'meal/rate.html')
