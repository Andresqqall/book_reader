# Generated by Django 5.0.1 on 2024-01-10 07:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnalytic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_reading_time_7_days', models.DurationField()),
                ('total_reading_time_30_days', models.DurationField()),
                ('avg_reading_time', models.DurationField()),
                ('min_reading_time', models.DurationField()),
                ('max_reading_time', models.DurationField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
