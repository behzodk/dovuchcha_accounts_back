# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubdomainViewSet, UserSubdomainsView

router = DefaultRouter()
router.register(r'subdomains', SubdomainViewSet, basename='subdomain')

urlpatterns = [
    path('', include(router.urls)),
    path('subdomains/users/<int:user_id>/', UserSubdomainsView.as_view(), name='user-subdomains'),
]