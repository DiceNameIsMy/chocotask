from django.urls import path, include

from .views import SignInView, SignUpView, RefreshTokenView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('token/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
]
