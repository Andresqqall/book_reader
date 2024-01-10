from django.urls import reverse
from rest_framework import status

from apps_generic.whodidit.test import BaseUserAuth


class TestUserSelfAPIView(BaseUserAuth):
    url = reverse('self_user')

    def test_authenticated_user_can_get_object(self, client, authenticate_user):
        """
        Test that an authenticated user can successfully retrieve their own user information.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        response_data = [response.json()]
        assert len(response_data) == 1

    def test_unauthenticated_user_cannot_get_object(self, client):
        """
        Test that an unauthenticated user cannot retrieve user information and receives a 401 Unauthorized response.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
