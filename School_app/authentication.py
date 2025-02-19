import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No token provided, no authentication.

        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Authorization header must start with "Bearer "')

        token = auth_header[7:]  # Remove "Bearer " part from the token

        try:
            # Decode the token using the secret key and verify it
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Check if token is expired
            if payload['exp'] < datetime.utcnow():
                raise AuthenticationFailed('Token has expired')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid')

        # If the token is valid, find the user associated with it
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, token)  # Return the user and the token to DRF
