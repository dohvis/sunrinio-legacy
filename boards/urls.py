from django.conf.urls import url

from boards import views


urlpatterns = [
    url(r'^$', views.board_list, name='list'),
    url(r'^(?P<board_pk>\d+)/$', views.post_list, name='post_list'),
    url(r'^(?P<board_pk>\d+)/write/$', views.post_write, name='post_write'),
    url(r'^(?P<board_pk>\d+)/(?P<post_pk>\d+)/$', views.post_view, name='post_view'),
]
