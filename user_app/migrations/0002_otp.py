# Generated by Django 5.0.2 on 2024-04-19 17:23

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code1', models.CharField(default='3d', max_length=1)),
                ('code2', models.CharField(default='4e', max_length=1)),
                ('code3', models.CharField(default='32', max_length=1)),
                ('code4', models.CharField(default='21', max_length=1)),
                ('verify', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('exp', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
