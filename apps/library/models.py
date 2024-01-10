from django.contrib.auth import get_user_model
from django.db import models

from apps.books.models import Book

# Create your models here.
User = get_user_model()


class SavedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class ReadingSession(models.Model):
    saved_book = models.ForeignKey(to=SavedBook, related_name='saved_book', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True, editable=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.saved_book.user.username} - {self.saved_book.book.title} - {self.start_time}"
