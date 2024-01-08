from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from apps.users.serializers import UserSerializer

# Create your views here.

User = get_user_model()


class UserSelfAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User, id=getattr(self.request.user, 'id', None))
