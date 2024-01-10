from datetime import datetime

from rest_framework import generics
from rest_framework.generics import get_object_or_404

from apps.library.models import SavedBook, ReadingSession
from apps.library.serializers import SavedBookDetailSerializer, SavedBookCreateSerializer, SavedBookUpdateSerializer


class SavedBookListCreateAPIView(generics.ListCreateAPIView):
    """
        List and create SavedBook objects.
    """
    read_serializer_class = SavedBookDetailSerializer
    serializer_class = read_serializer_class
    write_serializer_class = SavedBookCreateSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return self.write_serializer_class
        return self.read_serializer_class

    def get_queryset(self):
        return SavedBook.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class SavedBookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update, and delete a SavedBook object.
    """
    serializer_class = SavedBookUpdateSerializer
    lookup_url_kwarg = 'id'

    def get_object(self):
        return get_object_or_404(SavedBook, id=self.kwargs.get('id', None), user=self.request.user)

    def perform_update(self, serializer):
        if 'open' in serializer.validated_data:

            reading_session = ReadingSession.objects.filter(
                saved_book__user=self.request.user, end_time__isnull=True
            )
            if reading_session.exists():
                reading_session.update(
                    end_time=datetime.now()
                )

            if serializer.validated_data.pop('open'):
                ReadingSession.objects.create(saved_book=serializer.instance)

        serializer.save()
