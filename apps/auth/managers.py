from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce
from django.utils import timezone


class OTCManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            active_to=Coalesce(
                F('created_on', ) + timezone.timedelta(hours=1), F('created_on'),
                output_field=models.DateTimeField()
            )
        )
