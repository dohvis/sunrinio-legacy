from django.conf.urls import url

from accounts import views

urlpatterns = [
    url('^login/', views.login, name='login'),
    url('^logout/', views.logout, name='logout'),
    url('^signup/', views.signup, name='signup'),
    url('^update_profile_image/', views.update_profile_image),
]
