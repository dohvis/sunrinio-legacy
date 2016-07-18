from django.conf.urls import url

from tags import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.tag_detail, name='detail'),
]
