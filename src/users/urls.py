from django.conf.urls import url
from django.urls import include

urlpatterns = [
    # url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
]
