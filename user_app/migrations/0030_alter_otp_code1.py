# Generated by Django 5.0.2 on 2024-05-06 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0029_alter_otp_code1_giftcardbuying_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='0e2d96', max_length=6),
        ),
    ]
