from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


UserModel = get_user_model()


class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True, write_only=True)

    def authenticate(self) -> UserModel:
        user = authenticate(**self.validated_data)
        return user


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        required=True,
        validators=(
            UniqueValidator(
                queryset=UserModel.objects.all(),
            ),
        ),
    )
    password1 = serializers.CharField(max_length=100, required=True, write_only=True)
    password2 = serializers.CharField(max_length=100, required=True, write_only=True)
    email = serializers.EmailField(required=False)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")

        return attrs

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            email=validated_data.get('email', None),
        )
        return user

    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2', 'email')
