from django.conf.urls import url
from teams import views

urlpatterns = [
    url(r'^(?P<team_id>\d+)/want2join/$', views.Want2JoinView.as_view()),
]
