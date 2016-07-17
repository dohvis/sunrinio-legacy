from django.conf.urls import url

from teams import views

urlpatterns = [
    url(r'^$', views.team_list, name='list'),
    url(r'^add/$', views.team_add, name='add'),
    url(r'^(?P<pk>\d+)/$', views.team_detail, name='detail'),
    url(r'^(?P<pk>\d+)/members/(?P<user_pk>\d+)/delete/$', views.team_member_delete, name='member-delete'),
    url(r'^(?P<pk>\d+)/joins/(?P<user_pk>\d+)/accept/$', views.team_join_request_accept, name='accept'),
    url(r'^(?P<pk>\d+)/joins/(?P<user_pk>\d+)/reject/$', views.team_join_request_reject, name='reject'),
    url(r'^(?P<pk>\d+)/join/$', views.team_join, name='join'),

]
