from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.authentication import create_or_recreate_token

from .serializers import UserSignInSerializer, UserSignUpSerializer


UserModel = get_user_model()


class SignInView(GenericAPIView):
    serializer_class = UserSignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.authenticate()
        if not user:
            return Response(
                {'detail': 'Invalid Credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token = create_or_recreate_token(user)

        data = self.get_response_data(serializer, token)
        return Response(data=data, status=status.HTTP_200_OK)

    def get_response_data(self, serializer, token: Token) -> dict:
        return {
            'user': serializer.data,
            'expires_in': settings.TOKEN_EXPIRATION,
            'token': token.key,
        }


class SignUpView(GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = Token.objects.create(user=user)
        data = self.get_response_data(serializer, token)
        return Response(data=data, status=status.HTTP_201_CREATED)

    def get_response_data(self, serializer, token: Token) -> dict:
        return {
            'user': serializer.data,
            'expires_in': settings.TOKEN_EXPIRATION,
            'token': token.key,
        }


class RefreshTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        Delete old token and create new
        with extended expiration date
        """
        token: Token = request.auth
        token.delete()
        new_token = Token.objects.create(user=token.user)
        return Response(
            {
                'token': new_token.key,
                'expires_in': settings.TOKEN_EXPIRATION,
            },
            status=status.HTTP_201_CREATED,
        )
