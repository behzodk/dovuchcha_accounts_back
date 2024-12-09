from rest_framework import viewsets
from .models import Subdomain
from .serializers import SubdomainSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response

class SubdomainViewSet(viewsets.ModelViewSet):
    queryset = Subdomain.objects.exclude(status='pending').order_by('-created_at')
    serializer_class = SubdomainSerializer


class UserSubdomainsView(APIView):

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        user_subdomains = Subdomain.objects.filter(user=user)

        serializer = SubdomainSerializer(user_subdomains, many=True)
        return Response(serializer.data)