from django.contrib import admin

from apps.library.models import ReadingSession, SavedBook

# Register your models here.

admin.site.register(SavedBook)
admin.site.register(ReadingSession)
