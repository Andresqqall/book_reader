from datetime import datetime, timedelta

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from apps.analytics.models import UserAnalytic
from apps.analytics.tasks import calculate_reading_time, collect_analytics
from apps.library.models import ReadingSession
from apps.library.tests import BasUserSavedBook
from apps_generic.whodidit.test import BaseUserAuth


class TestUserAnalyticRetrieveAPIView(BaseUserAuth):
    """
    Tests for the UserAnalyticRetrieveAPIView.
    """
    url = reverse('self_analytic')

    def test_authenticated_user_can_retrieve_analytics(self, client, authenticate_user, base_user_analytic):
        """
        Test that an authenticated user can successfully retrieve their analytics.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) >= 1

    def test_unauthenticated_user_cannot_retrieve_analytics(self, client):
        """
        Test that an unauthenticated user cannot retrieve analytics.
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.fixture
    def base_user_analytic(self, authenticate_user):
        """
        Fixture to create a base UserAnalytic for testing.
        """
        return UserAnalytic.objects.create(user=authenticate_user)


class TestCollectAnalytics(BasUserSavedBook):
    """
    Tests for the `calculate_reading_time` and `collect_analytics` functions.
    """

    @pytest.fixture
    def create_reading_session(self, authenticate_user, base_saved_book):
        """
        Fixture to create a reading session for testing.
        """
        now = datetime.now()
        return ReadingSession.objects.create(
            saved_book=base_saved_book,
            start_time=now - timedelta(days=15),
            end_time=now
        )

    def test_calculate_reading_time(self, authenticate_user, create_reading_session):
        """
        Test the `calculate_reading_time` function.
        """
        analytics = calculate_reading_time(authenticate_user)

        assert 'total_reading_time_7_days' in analytics
        assert 'total_reading_time_30_days' in analytics
        assert 'avg_reading_time' in analytics
        assert 'min_reading_time' in analytics
        assert 'max_reading_time' in analytics

    @pytest.mark.django_db
    def test_collect_analytics(self, authenticate_user, create_reading_session):
        """
        Test the `collect_analytics` task.
        """
        collect_analytics()

        user_analytic = UserAnalytic.objects.get(user=authenticate_user)

        assert user_analytic.total_reading_time_7_days is not None
        assert user_analytic.total_reading_time_30_days is not None
        assert user_analytic.avg_reading_time is not None
        assert user_analytic.min_reading_time is not None
        assert user_analytic.max_reading_time is not None
