# Generated by Django 5.0.2 on 2024-04-26 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0012_coins_alter_otp_code1'),
    ]

    operations = [
        migrations.AddField(
            model_name='coins',
            name='buyin_rate',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='coins',
            name='buying_quantity',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AddField(
            model_name='coins',
            name='selling_quantity',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AddField(
            model_name='coins',
            name='selling_rate',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='e4b00f', max_length=6),
        ),
    ]
