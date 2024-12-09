from rest_framework import serializers
from .models import Subdomain
from django.contrib.auth.models import User

class SubdomainSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Subdomain
        fields = '__all__'