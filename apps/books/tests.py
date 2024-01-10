from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from apps.books.models import Author, Book
from apps_generic.whodidit.test import BaseUserAuth


class BaseBook:
    @pytest.fixture
    def base_author(self):
        return Author.objects.create(
            first_name='Test Author First NAME',
            last_name='Test Author Last Name',
            description='Description'
        )

    @pytest.fixture
    def base_book(self, base_author):
        book = Book.objects.create(
            title='Test Author First NAME',
            publication_year=datetime.now(),
            short_description='Short Description',
            full_description='Full Description'
        )
        book.author.add(base_author)
        return book


class TestBookListAPIView(BaseUserAuth, BaseBook):
    url = reverse('books_list')

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
