from rest_framework import serializers

from apps.analytics.models import UserAnalytic


class UserAnalyticDetailSerializer(serializers.ModelSerializer):
    """
        Serializer for detailed representation of SavedBook
    """

    class Meta:
        model = UserAnalytic
        fields = [
            'id', 'user', 'total_reading_time_7_days', 'total_reading_time_30_days',
            'avg_reading_time', 'min_reading_time', 'max_reading_time'
        ]
