# Generated by Django 5.0.1 on 2024-01-07 21:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationTry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegisterOTC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='when created')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='when updated')),
                ('code', models.CharField(max_length=6, unique=True)),
                ('applied_date', models.DateTimeField(blank=True, null=True)),
                ('created_by',
                 models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                   related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL,
                                   verbose_name='who created')),
                ('updated_by',
                 models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                   related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL,
                                   verbose_name='when updated')),
                ('registration_try',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_auth.registrationtry')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SetEmailOTC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='when created')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='when updated')),
                ('code', models.CharField(max_length=6, unique=True)),
                ('applied_date', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('created_by',
                 models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                   related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL,
                                   verbose_name='who created')),
                ('updated_by',
                 models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                   related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL,
                                   verbose_name='when updated')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
