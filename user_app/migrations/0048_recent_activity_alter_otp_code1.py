# Generated by Django 5.0.2 on 2024-07-12 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0047_balance_history_proof_alter_otp_code1'),
    ]

    operations = [
        migrations.CreateModel(
            name='recent_activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.FileField(upload_to='ract/')),
                ('amount', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='otp',
            name='code1',
            field=models.CharField(default='abdd63', max_length=6),
        ),
    ]
