# Generated by Django 5.0.2 on 2024-07-16 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0053_recent_activity_a_id_alter_otp_code1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='680b6f', max_length=6),
        ),
    ]
