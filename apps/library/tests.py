import pytest
from django.urls import reverse
from rest_framework import status

from apps.books.tests import BaseBook
from apps.library.models import SavedBook, ReadingSession
from apps_generic.whodidit.test import BaseUserAuth


class TestSavedBookListCreateAPIView(BaseUserAuth, BaseBook):
    url = reverse('library')

    def test_authenticated_user_can_get_queryset(self, client, authenticate_user, base_book):
        """
        Test that an authenticated user can successfully retrieve a queryset of books
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) >= 1

    def test_unauthenticated_user_cannot_get_queryset(self, client):
        """
        Test that an unauthenticated user cannot retrieve the queryset of books
        and receives a 401 Unauthorized response
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_create_saved_book(self, client, authenticate_user, base_book):
        """
        Test that an authenticated user can successfully create a saved book.
        """
        response = client.post(self.url, data=dict(user=authenticate_user.id, book=base_book.id))
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.json()) >= 1

    def test_unauthenticated_user_cannot_create_saved_book(self, client):
        """
        Test that an unauthenticated user cannot create a saved book and receives a 401 Unauthorized response
        """
        response = client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_existing_book(self, client, authenticate_user, base_book):
        """
        Test that creating a saved book with an already existing combination of user
        and book results in a 400 Bad Request response
        """
        base_payload = dict(user=authenticate_user.id, book=base_book.id)

        # Create a saved book with the specified user and book
        response = client.post(self.url, data=base_payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.json()) >= 1

        # Attempt to create the same saved book again
        response = client.post(self.url, data=base_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'book': ['Book already exists']}


class BasUserSavedBook(BaseUserAuth, BaseBook):

    @pytest.fixture
    def base_saved_book(self, authenticate_user, base_book):
        """
        Fixture to create a SavedBook instance for testing.
        """
        return SavedBook.objects.create(
            user=authenticate_user,
            book=base_book
        )


class TestReadingSessionCreateAPIView(BasUserSavedBook):

    def test_authenticated_user_can_create_saved_book(self, client, authenticate_user, base_saved_book):
        """
        Test that an authenticated user can create a saved book with 'open' set to True.
        """
        self.send_patch_method(client, authenticate_user, base_saved_book, dict(open=True))

    def test_closed_reading_session(self, client, authenticate_user, base_saved_book):
        """
        Test creating a reading session with 'open' set to True, then closing it.
        """
        self.send_patch_method(client, authenticate_user, base_saved_book, dict(open=True))

        # Check that the reading session is created
        reading_session = ReadingSession.objects.filter(
            saved_book=base_saved_book, end_time__isnull=True
        )
        assert reading_session.exists() is True

        # Test closing the reading session by setting 'open' to False
        self.send_patch_method(client, authenticate_user, base_saved_book, dict(open=False))

        # Check that the reading session is closed
        reading_session = ReadingSession.objects.filter(
            saved_book=base_saved_book, end_time__isnull=True
        )
        assert reading_session.exists() is False

    @staticmethod
    def send_patch_method(client, authenticate_user, base_saved_book, data):
        """
        Helper method to send a PATCH request to the API endpoint.
        """
        url = reverse('update_library', kwargs={'id': int(base_saved_book.id)})
        response = client.patch(url, data=data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) >= 1
