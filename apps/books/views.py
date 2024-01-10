from rest_framework import generics

from apps.books.models import Book
from apps.books.serializers import BookDetailSerializer


class BookListAPIView(generics.ListAPIView):
    """
      List all Book objects.
    """
    serializer_class = BookDetailSerializer

    def get_queryset(self):
        return Book.objects.all()
