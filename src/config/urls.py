from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpaatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),

    path('api/', include('wallets.urls')),
]

# Documentation
urlpatterns += doc_urls

# Debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
