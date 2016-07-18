from django.shortcuts import render, HttpResponse
from .models import Openchat


def openchat_view(request):
    context_data = {'chats': Openchat.objects.all()}
    return render(request, 'openchat/list.html', context_data)


def add(request):
    url = request.GET['url']
    Openchat.objects.create(user=request.user, url=url, description=request.user.username + " 오픈채팅")
    return HttpResponse(status=200)
