from rest_framework import generics
from rest_framework.generics import get_object_or_404

from apps.analytics.models import UserAnalytic
from apps.analytics.serializers import UserAnalyticDetailSerializer


class UserAnalyticRetrieveAPIView(generics.RetrieveAPIView):
    """
        Retrieves analytics for the authenticated user.
    """
    serializer_class = UserAnalyticDetailSerializer

    def get_object(self):
        return get_object_or_404(UserAnalytic, user=getattr(self.request.user, 'id', None))
