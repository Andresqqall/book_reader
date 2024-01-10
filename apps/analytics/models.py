from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class UserAnalytic(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    total_reading_time_7_days = models.DurationField(null=True)
    total_reading_time_30_days = models.DurationField(null=True)
    avg_reading_time = models.DurationField(null=True)
    min_reading_time = models.DurationField(null=True)
    max_reading_time = models.DurationField(null=True)
