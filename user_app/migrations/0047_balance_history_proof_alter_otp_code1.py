# Generated by Django 5.0.2 on 2024-07-10 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0046_balance_history_amount_alter_otp_code1'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance_history',
            name='proof',
            field=models.FileField(default=1, upload_to='bproof/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='7b3993', max_length=6),
        ),
    ]
