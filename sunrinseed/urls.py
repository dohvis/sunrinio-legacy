"""sunrinseed URL Configuration

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
from tags import views as tags_views
from teams import views as teams_views
from dinner import views as dinner_views
from meals import views as meal_views
from utils import views as util_views

from sunrinseed.settings import base as settings

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

join_urls = DefaultRouter()
join_urls.register(r'^', teams_views.Want2JoinViewSet)

urlpatterns = [
    url(r'^api/teams/(?P<pk>\d+)/join', include(join_urls.urls)),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^api/', include(router.urls)),

    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/auth/facebook/$', accounts_views.FacebookLogin.as_view(), name='fb_login'),

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(accounts_urls, namespace='accounts')),
    url(r'^allauth/', include('allauth.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^debug/(?P<dir_name>\w+)/(?P<template_name>\w+)/$', util_views.template_debug),

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
