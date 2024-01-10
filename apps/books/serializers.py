from rest_framework import serializers

from apps.books.models import Book, Author


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
        Serializer for detailed representation of Author
    """

    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'last_name', 'description'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    """
        Serializer for detailed representation of a Book
    """

    class Meta:
        model = Book
        fields = [
            'id', 'author', 'title', 'publication_year', 'short_description', 'full_description'
        ]

    author = AuthorDetailSerializer(many=True, default=None)
