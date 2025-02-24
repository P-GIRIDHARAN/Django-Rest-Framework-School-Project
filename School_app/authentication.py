import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the Authorization header (Bearer <token>)
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No token provided, so return None

        token = auth_header.split(' ')[1] if ' ' in auth_header else None

        if not token:
            raise exceptions.AuthenticationFailed('Authorization token not found')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, token)  # Return the user and token as a tuple
