from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from .models import CustomUser


def create_or_recreate_token(user: CustomUser) -> Token:
    """
    If user have token delete it. Return new token
    """
    token, created = Token.objects.get_or_create(user=user)
    if not created:
        token.delete()
        token = Token.objects.create(user=user)
    return token


class ExpiringTokenAuthentication(TokenAuthentication):
    """ 
    Implements token expiration.

    in settings.py add -> TOKEN_EXPIRATION: timedelta()
    """
    TOKEN_EXPIRES_IN: timedelta = settings.TOKEN_EXPIRATION

    def authenticate_credentials(self, key) -> tuple[CustomUser, Token]:
        credentails = super().authenticate_credentials(key)

        is_expired = self.token_is_expired(credentails[1])
        if is_expired:
            credentails[1].delete()
            raise AuthenticationFailed('The Token is expired')
        
        return credentails
    
    def token_is_expired(self, token) -> bool:
        """
        Returns True if the token is expired and False otherwise.
        """
        return token.created < (timezone.now() - self.TOKEN_EXPIRES_IN)
    
