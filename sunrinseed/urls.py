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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from accounts import urls as accounts_urls
from accounts import views as accounts_views
from teams import urls as teams_urls
from teams import views as teams_views
from dinner import views as dinner_views

from sunrinseed.settings import base as settings

router = DefaultRouter()
router.register(r'users', accounts_views.UserViewSet)
router.register(r'tags', accounts_views.TagViewSet)
router.register(r'teams', teams_views.TeamViewSet)
router.register(r'dinners', dinner_views.DinnerViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/auth/facebook/$', accounts_views.FacebookLogin.as_view(), name='fb_login'),

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(accounts_urls)),

    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^team/', include(teams_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
