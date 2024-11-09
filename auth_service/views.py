from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.models import Application, AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from oauth2_provider.settings import oauth2_settings
from django.utils import timezone
import secrets


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)

        try:
            app = Application.objects.get(name='dovuchcha_auth')
        except Application.DoesNotExist:
            return Response({'error': 'OAuth application not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        AccessToken.objects.filter(user=user, application=app).delete()
        RefreshToken.objects.filter(user=user, application=app).delete()

        token = AccessToken.objects.create(
            token=secrets.token_urlsafe(32),
            user=user,
            application=app,
            expires=timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            scope='read write'
        )

        refresh_token = RefreshToken.objects.create(
            user=user,
            application=app,
            token=secrets.token_urlsafe(32),
            access_token=token
        )

        return Response({
            'access_token': token.token,
            'token_type': 'Bearer',
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'refresh_token': refresh_token.token,
            'scope': token.scope,
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })