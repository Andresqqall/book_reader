from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.response import Response

from apps.auth.jwt_auth import generate_access_token
from apps.auth.models import RegisterOTC
from apps.auth.serializers import (
    LoginSerializer, UserRegistrationSerializer, ConfirmRegistrationSerializer
)
from utils.encoding_values import get_encoded_value

User = get_user_model()


def get_jwt_tokens(user):
    return {
        'access_token': generate_access_token(user),
        'refresh_token': generate_access_token(user, token_type='refresh')
    }


class LoginAPIView(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = ()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return Response(
            data=get_jwt_tokens(user),
            status=status.HTTP_201_CREATED
        )


class RegisterUserAPIView(generics.CreateAPIView):
    """
    Register user is the first step of registration
    """
    permission_classes = []
    authentication_classes = ()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        register_otc = RegisterOTC.objects.create(registration_try=instance)
        signed_value = get_encoded_value(register_otc.id)

        return Response(
            data={'token': signed_value},
            status=status.HTTP_201_CREATED
        )


class ConfirmRegistrationAPIView(generics.CreateAPIView):
    """

        Confirm Registration APIView

        2 step

        # POST Example:

            {
              "token": "MjYuZEFPS2Q2Vy1kVTlGZUE5SGdsek10UzZjdG1EbTY4T28zZ0Qwb2lhSGxlQQ==",
              "code": "096431",

              "password1": "!z9Yf3^V5%Ob9",
              "password2": "!z9Yf3^V5%Ob9",

              # Personal info
              "first_name": "string",
              "last_name": "string"
            }
    """
    permission_classes = []
    authentication_classes = ()
    serializer_class = ConfirmRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.pop('otc').apply(
            password=serializer.validated_data.pop('password1')
        )

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        User.objects.filter(id=user.id).update(**serializer.validated_data)

        return Response(
            data=get_jwt_tokens(user),
            status=status.HTTP_201_CREATED
        )
