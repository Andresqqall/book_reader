from rest_framework import serializers

from apps.library.models import SavedBook


class SavedBookPrimaryField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return SavedBook.objects.filter(user=self.context["request"].user)
