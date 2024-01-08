from apps_generic.whodidit.test import *
from django.urls import reverse
from rest_framework import status
import pytest


class TestUserSelfAPIView:
    url = reverse('self_user')

    @pytest.mark.django_db
    def test_authenticated_user_can_get_object(self, client, authenticated_user):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_unauthenticated_user_cannot_get_object(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
