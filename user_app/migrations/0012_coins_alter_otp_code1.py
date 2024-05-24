# Generated by Django 5.0.2 on 2024-04-26 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0011_kycverification_status_kycverification_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='coins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.FileField(upload_to='coins/')),
            ],
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='9f6098', max_length=6),
        ),
    ]
