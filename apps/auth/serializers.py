from django.contrib.auth import get_user_model
from django.core.signing import BadSignature
from rest_framework import serializers

from apps.auth.models import RegistrationTry, RegisterOTC
from utils.encoding_values import get_decoded_value
from datetime import datetime
User = get_user_model()


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get('email'))
        self.validate_user_existence(user)
        self.validate_user_password(user, attrs)
        attrs['user'] = user
        return attrs

    @staticmethod
    def validate_user_existence(user: User):
        if not user.exists():
            raise serializers.ValidationError(
                {'non_field_error': ["User not found"]}
            )

    @staticmethod
    def validate_user_password(user: User, attrs):
        if not user.check_password(attrs.get('password')):
            raise serializers.ValidationError(
                {'password': ["No account found with the given credentials"]}
            )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationTry
        fields = ['email', ]

    email = serializers.EmailField(write_only=True)

    @staticmethod
    def validate_email(value):
        user = User.objects.filter(email=value)
        if user.exists():
            raise serializers.ValidationError(detail="User already exists")
        return value


class ConfirmRegistrationSerializer(serializers.Serializer):
    token = serializers.CharField()

    password1 = serializers.CharField()
    password2 = serializers.CharField()

    code = serializers.CharField(max_length=6)

    # Personal information
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)

    def validate(self, attrs):
        self.validate_password(attrs)

        otc = RegisterOTC.objects.filter(
            id=attrs.pop('token'),
            applied_date__isnull=True,
            active_to__gte=datetime.now()
        )
        otc_instance = otc.first()

        self.validate_token_expiration(otc)
        self.validate_match_code(attrs, otc_instance.code)

        attrs['otc'] = otc_instance
        return attrs

    @staticmethod
    def validate_token(value):
        try:
            object_id = get_decoded_value(value)
        except BadSignature:
            raise serializers.ValidationError(detail="Token is not valid")
        return int(object_id)

    @staticmethod
    def validate_token_expiration(otc_instance):
        if not otc_instance.exists():
            raise serializers.ValidationError(
                {'token': ["Token is expired try resend"]}
            )

    @staticmethod
    def validate_match_code(attrs, white_code):
        if attrs.pop('code') != white_code:
            raise serializers.ValidationError(
                {'code': ["Wrong code please try again"]}
            )

    @staticmethod
    def validate_password(attrs):
        errors = dict()
        if attrs.get('password1') != attrs.pop('password2'):
            errors['password2'] = 'Passwords didn\'t match'
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class JWTTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
