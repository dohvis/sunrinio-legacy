from django.conf.urls import include, url

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
]
