# Generated by Django 5.0.2 on 2024-07-18 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0057_rename_airtime_p_network_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='order',
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='7c093c', max_length=6),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
