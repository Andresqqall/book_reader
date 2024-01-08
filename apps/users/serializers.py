from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Base representation of user serializer
    """

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name'
        ]

    first_name = serializers.CharField(min_length=5, max_length=150)
    last_name = serializers.CharField(min_length=5, max_length=150)
