# Generated by Django 3.1.7 on 2021-10-09 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0009_auto_20211005_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='lock_status',
            field=models.BooleanField(default=False),
        ),
    ]
