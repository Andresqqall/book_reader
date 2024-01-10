from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum, ExpressionWrapper, F, DurationField, Avg, Max, Min, Case, When, Value

from apps.analytics.models import UserAnalytic
from apps.library.models import ReadingSession
from book_reader.celery import app

User = get_user_model()


@app.task
def collect_analytics():
    """
    Task to collect and update user analytics for reading sessions.
    """
    users = User.objects.filter(is_active=True)

    for user in users:
        total_reading_time_7_days = calculate_reading_time(user)
        UserAnalytic.objects.update_or_create(user=user, defaults=total_reading_time_7_days)


def calculate_reading_time(user: User):
    """
    Calculate reading time analytics for a user.

    Parameters:
        user (User): The user for whom to calculate analytics.

    Returns:
        dict: A dictionary containing various reading time analytics.
    """
    now = datetime.now()
    start_date_7_days = now - timedelta(days=7)
    start_date_30_days = now - timedelta(days=30)

    reading_sessions = ReadingSession.objects.filter(
        saved_book__user=user, start_time__gte=start_date_30_days, end_time__isnull=False
    ).annotate(
        reading_time=ExpressionWrapper(
            F('end_time') - F('start_time'),
            output_field=DurationField()
        )
    ).aggregate(
        total_reading_time_7_days=Sum(
            Case(
                When(start_time__gte=start_date_7_days, then=F('reading_time')),
                default=Value(timedelta()), output_field=DurationField()
            )
        ),
        total_reading_time_30_days=Sum(
            Case(
                When(start_time__gte=start_date_30_days, then=F('reading_time')),
                default=Value(timedelta()), output_field=DurationField()
            )
        ),
        avg_reading_time=Avg(F('reading_time')),
        min_reading_time=Min(F('reading_time')),
        max_reading_time=Max(F('reading_time'))
    )
    return reading_sessions
