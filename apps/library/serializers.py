from rest_framework import serializers

from apps.books.serializers import BookDetailSerializer
from apps.library.models import SavedBook
from apps.users.serializers import UserSerializer


class SavedBookDetailSerializer(serializers.ModelSerializer):
    """
        Serializer for detailed representation of SavedBook
    """

    class Meta:
        model = SavedBook
        fields = [
            'id', 'user', 'book'
        ]

    user = UserSerializer()
    book = BookDetailSerializer()


class SavedBookCreateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating SavedBook
    """

    class Meta:
        model = SavedBook
        fields = [
            'id', 'book'
        ]

    @staticmethod
    def validate_book(value):
        saved_book = SavedBook.objects.filter(book_id=value.id)
        if saved_book.exists():
            raise serializers.ValidationError(
                detail='Book already exists'
            )
        return value


class SavedBookUpdateSerializer(serializers.ModelSerializer):
    """
        Serializer for update SavedBook
    """

    class Meta:
        model = SavedBook
        fields = [
            'id', 'open'
        ]

    open = serializers.BooleanField(default=False)
