from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_service.urls')),
    path('api/', include('subdomains.urls')),
]
