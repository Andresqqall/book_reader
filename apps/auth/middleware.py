import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework import exceptions
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

User = get_user_model()


class VerifyJWT(VerifyJSONWebTokenSerializer):
    def validate(self, attrs):

        token = attrs['token']

        payload = self._check_payload(token=token)
        if payload['token_type'] == 'refresh':
            user = AnonymousUser()
        else:
            user = self._check_user(payload=payload)
            if user and user.change_password_at and \
                    datetime.datetime.timestamp(user.change_password_at) > payload['iat']:
                msg = 'Signature has expired.'
                raise exceptions.AuthenticationFailed(msg)

        return {
            'token': token,
            'user': user,
            'iat': payload['iat'],
            'exp': payload['exp']
        }


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """ Middleware for authenticating JSON Web Tokens in Authorize Header """

    def process_request(self, request):
        request.user = self.__class__.get_user_jwt(request)

    @staticmethod
    def get_user_jwt(request):
        """
        Inspects the token for the user. Otherwise it defaults to AnonymousUser.
        Returns: instance of user object or AnonymousUser object
        """
        if request.user.is_anonymous:
            try:
                token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                data = {'token': token}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                token_user = valid_data['user']
                user = token_user if token_user.is_active else None
            except:
                return AnonymousUser()
            return user or AnonymousUser()
        return request.user
