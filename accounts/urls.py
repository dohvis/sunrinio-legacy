from django.conf.urls import url

from accounts import views

urlpatterns = [
    url('^signin/', views.signin),
    url('^update_profile_image/', views.update_profile_image),
]
