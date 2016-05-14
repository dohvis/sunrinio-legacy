from django.conf.urls import url

from accounts import views

urlpatterns = [
    url('^signin/', views.signin),
]
