from django.conf.urls import url

from accounts import views

urlpatterns = [
    url('^login/', views.login, name='login'),
    url('^update_profile_image/', views.update_profile_image),
]
