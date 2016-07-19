"""sunrinio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from accounts import urls as accounts_urls
from accounts import views as accounts_views
from hotplace import views as place_views
from boards import views as boards_views
from schedule import views as schedule_views
from tags import urls as tags_urls
from tags import views as tags_views
from teams import urls as teams_urls
from teams import views as teams_views
from dinner import views as dinner_views
from meals import views as meal_views
from utils import views as util_views
from openchat import views as open_views
from sunrinio import views as index_views

from sunrinio.settings import base as settings

router = DefaultRouter()
router.register(r'users', accounts_views.UserViewSet)
router.register(r'tags', tags_views.TagViewSet)
router.register(r'teams', teams_views.TeamViewSet)
router.register(r'dinners', dinner_views.DinnerViewSet)
router.register(r'places', place_views.PlaceViewSet)
router.register(r'reviews', place_views.ReviewViewSet)
router.register(r'boards', boards_views.BoardViewSet)
router.register(r'posts', boards_views.PostViewSet)
router.register(r'schedule', schedule_views.ScheduleViewSet)

urlpatterns = [
    url(r'^api/teams/(?P<pk>\d+)/join',
        teams_views.Want2JoinViewSet.as_view(actions={'get': 'list', 'post': 'create'})),
    url(r'^api/users/(?P<pk>\d+)/profile_image', accounts_views.get_profile_image),

    url(r'^$', index_views.index, name='index'),
    url(r'^api/', include(router.urls)),

    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/auth/facebook/$', accounts_views.FacebookLogin.as_view(), name='fb_login'),

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(accounts_urls, namespace='accounts')),

    url(r'^board/(?P<board_pk>\d+)/write', boards_views.post_write),
    url(r'^board/(?P<board_pk>\d+)/(?P<post_pk>\d+)', boards_views.post_view),
    url(r'^board/(?P<board_pk>\d+)/list/(?P<page_idx>\d+)', boards_views.post_list),
    url(r'^teams/', include(teams_urls, namespace='teams')),
    url(r'^tags/', include(tags_urls, namespace='tags')),
    url(r'^allauth/', include('allauth.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^debug/(?P<dir_name>\w+)/(?P<template_name>\w+)/$', util_views.template_debug),
    url(r'hotplace/$', place_views.mapview),
    url(r'hotplace/(?P<place_pk>\d+)/$', place_views.place_detail),
    url(r'hotplace/(?P<place_pk>\d+)/review/$', place_views.add_review),

    url(r'openchat/$', open_views.openchat_view),
    url(r'openchat/add/$', open_views.add),

    url(r'^meal/', meal_views.meal_view),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
