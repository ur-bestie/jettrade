# Generated by Django 5.0.2 on 2024-06-25 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0041_datapurchase_alter_otp_code1'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DataPurchase',
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='f1807e', max_length=6),
        ),
    ]
