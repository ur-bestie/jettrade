# Generated by Django 5.0.2 on 2024-07-19 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0060_rename_transaction_airtime_transaction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance_history',
            name='name',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='38a50e', max_length=6),
        ),
    ]
