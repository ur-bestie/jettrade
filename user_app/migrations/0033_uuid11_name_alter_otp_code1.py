# Generated by Django 5.0.2 on 2024-05-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0032_uuid11_alter_otp_code1'),
    ]

    operations = [
        migrations.AddField(
            model_name='uuid11',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='0858eb', max_length=6),
        ),
    ]
