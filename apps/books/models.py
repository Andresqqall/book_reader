from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    author = models.ManyToManyField(to=Author, related_name='book_author')
    title = models.CharField(max_length=255)
    publication_year = models.DateTimeField()
    short_description = models.TextField()
    full_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} Author: {self.author}"
