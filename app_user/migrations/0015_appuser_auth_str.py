# Generated by Django 3.1.7 on 2021-11-01 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0014_auto_20211101_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='auth_str',
            field=models.CharField(default='none', max_length=500),
        ),
    ]