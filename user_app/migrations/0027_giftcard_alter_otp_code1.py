# Generated by Django 5.0.2 on 2024-05-04 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0026_rename_buying_rate_setup_crypto_buying_rate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='giftcard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.FileField(upload_to='giftcard/')),
            ],
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='d9ee8f', max_length=6),
        ),
    ]
