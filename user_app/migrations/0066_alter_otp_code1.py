# Generated by Django 5.0.2 on 2024-07-22 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0065_remove_dataplan_network_alter_otp_code1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='29ac9f', max_length=6),
        ),
    ]
