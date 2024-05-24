# Generated by Django 5.0.2 on 2024-04-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0016_paymentmethod_alter_otp_code1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='03d512', max_length=6),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='link',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
